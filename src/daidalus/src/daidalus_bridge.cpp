#include "daidalus/include/daidalus_bridge.h"
#include "Daidalus.h"
#include "rust/cxx.h"
#include <cmath>
#include <limits>
#include <string>

using namespace larcfm;

namespace {

constexpr double kTwoPi = 6.28318530717958647692;

bool finite_heading_rad(double x) {
    return std::isfinite(x) && !std::isnan(x);
}

double pick_horizontal_resolution(Daidalus* daa, bool right) {
    double r = daa->horizontalDirectionResolution(right, "rad");
    if (finite_heading_rad(r)) {
        return r;
    }
    r = daa->horizontalDirectionRawResolution(right, "rad");
    if (finite_heading_rad(r)) {
        return r;
    }
    return std::numeric_limits<double>::quiet_NaN();
}

double best_resolution_heading(Daidalus* daa) {
    bool pref = daa->preferredHorizontalDirectionRightOrLeft();
    double r = pick_horizontal_resolution(daa, pref);
    if (finite_heading_rad(r)) {
        return r;
    }
    r = pick_horizontal_resolution(daa, !pref);
    if (finite_heading_rad(r)) {
        return r;
    }
    return std::numeric_limits<double>::quiet_NaN();
}

void apply_narrow_band(float* lo, float* hi, double center_rad, double half_width_rad) {
    *lo = static_cast<float>(center_rad - half_width_rad);
    *hi = static_cast<float>(center_rad + half_width_rad);
}

/** rel_x, rel_z: horizontal vector from ownship toward reference intruder (for geometry fallback). */
void fill_horizontal_bands(
    Daidalus* daa,
    DaidalusResult& res,
    float vel_x,
    float vel_z,
    double rel_x,
    double rel_z) {
    if (res.alert_level <= 0) {
        return;
    }
    daa->forceHorizontalDirectionBandsComputation();
    const double own_hd = std::atan2(static_cast<double>(vel_x), -static_cast<double>(vel_z));

    int nb = daa->horizontalDirectionBandsLength();
    bool filled = false;
    if (nb > 0) {
        int idx_at = daa->indexOfHorizontalDirection(own_hd);
        if (0 <= idx_at && idx_at < nb &&
            daa->horizontalDirectionRegionAt(idx_at) == BandsRegion::NONE) {
            Interval interval = daa->horizontalDirectionIntervalAt(idx_at, "rad");
            res.min_safe_heading = (float)interval.low;
            res.max_safe_heading = (float)interval.up;
            filled = true;
        }
        if (!filled) {
            for (int i = 0; i < nb; ++i) {
                if (daa->horizontalDirectionRegionAt(i) != BandsRegion::NONE) continue;
                Interval interval = daa->horizontalDirectionIntervalAt(i, "rad");
                double span = interval.up - interval.low;
                if (span > 0.01 && span < 6.27) {
                    res.min_safe_heading = (float)interval.low;
                    res.max_safe_heading = (float)interval.up;
                    filled = true;
                    break;
                }
            }
        }
        if (!filled) {
            for (int i = 0; i < nb; ++i) {
                if (daa->horizontalDirectionRegionAt(i) == BandsRegion::NONE) {
                    Interval interval = daa->horizontalDirectionIntervalAt(i, "rad");
                    res.min_safe_heading = (float)interval.low;
                    res.max_safe_heading = (float)interval.up;
                    break;
                }
            }
        }
        double span = static_cast<double>(res.max_safe_heading) - static_cast<double>(res.min_safe_heading);
        if (span >= kTwoPi - 0.02) {
            res.min_safe_heading = 0.0f;
            res.max_safe_heading = 0.0f;
        }
    }
    if (res.min_safe_heading == 0.0f && res.max_safe_heading == 0.0f) {
        const double w = 0.35;
        double hres = best_resolution_heading(daa);
        if (finite_heading_rad(hres)) {
            apply_narrow_band(&res.min_safe_heading, &res.max_safe_heading, hres, w);
        } else {
            double horiz = std::hypot(rel_x, rel_z);
            if (horiz > 1.0) {
                double esc = std::atan2(rel_x, -rel_z) + 1.57079632679489661923;
                while (esc < 0.0) {
                    esc += kTwoPi;
                }
                while (esc >= kTwoPi) {
                    esc -= kTwoPi;
                }
                apply_narrow_band(&res.min_safe_heading, &res.max_safe_heading, esc, w);
            }
        }
    }
}

}  // namespace

DaidalusWrapper::DaidalusWrapper(const DaidalusCppTune& t) {
    daa = std::make_unique<Daidalus>();
    daa->set_DO_365B();
    if (t.distance_filter_m > 0.0f) {
        daa->setDistanceFilter(static_cast<double>(t.distance_filter_m));
    }
    if (t.lookahead_s > 0.0f) {
        daa->setLookaheadTime(static_cast<double>(t.lookahead_s), "s");
    }
    if (t.horizontal_nmac_m > 0.0f) {
        daa->setHorizontalNMAC(static_cast<double>(t.horizontal_nmac_m));
    }
}

DaidalusWrapper::~DaidalusWrapper() {}

DaidalusResult DaidalusWrapper::evaluate_pair(
    const Vec3F& pos_a, const Vec3F& vel_a,
    const Vec3F& pos_b, const Vec3F& vel_b) {
    DaidalusResult res;
    res.alert_level = 0;
    res.time_to_violation = -1.0f;
    res.min_safe_heading = 0.0f;
    res.max_safe_heading = 0.0f;

    daa->clear();
    daa->setOwnshipState("A",
        Position::makeXYZ(pos_a.x, "m", pos_a.y, "m", pos_a.z, "m"),
        Velocity::makeVxyz(vel_a.x, vel_a.y, "m/s", vel_a.z, "m/s"));
    daa->addTrafficState("B",
        Position::makeXYZ(pos_b.x, "m", pos_b.y, "m", pos_b.z, "m"),
        Velocity::makeVxyz(vel_b.x, vel_b.y, "m/s", vel_b.z, "m/s"));

    int ac_idx = daa->aircraftIndex("B");
    if (ac_idx <= 0) return res;

    int al = daa->alertLevel(ac_idx);
    if (al < 0) {
        al = 0;
    }
    res.alert_level = al;
    res.time_to_violation = (float)daa->timeToHorizontalClosestPointOfApproach(ac_idx);

    const double rel_x = static_cast<double>(pos_b.x - pos_a.x);
    const double rel_z = static_cast<double>(pos_b.z - pos_a.z);
    fill_horizontal_bands(daa.get(), res, vel_a.x, vel_a.z, rel_x, rel_z);

    return res;
}

DaidalusResult DaidalusWrapper::evaluate_multi(
    const Vec3F& pos_o,
    const Vec3F& vel_o,
    rust::Slice<const Vec3F> traffic_pos,
    rust::Slice<const Vec3F> traffic_vel) {
    DaidalusResult res;
    res.alert_level = 0;
    res.time_to_violation = -1.0f;
    res.min_safe_heading = 0.0f;
    res.max_safe_heading = 0.0f;

    const std::size_t n = traffic_pos.size();
    if (n == 0 || n != traffic_vel.size()) {
        return res;
    }

    daa->clear();
    daa->setOwnshipState("OWNSHIP",
        Position::makeXYZ(pos_o.x, "m", pos_o.y, "m", pos_o.z, "m"),
        Velocity::makeVxyz(vel_o.x, vel_o.y, "m/s", vel_o.z, "m/s"));

    for (std::size_t i = 0; i < n; ++i) {
        const Vec3F& p = traffic_pos[i];
        const Vec3F& v = traffic_vel[i];
        std::string tid = std::string("T") + std::to_string(i);
        daa->addTrafficState(tid,
            Position::makeXYZ(p.x, "m", p.y, "m", p.z, "m"),
            Velocity::makeVxyz(v.x, v.y, "m/s", v.z, "m/s"));
    }

    int al = daa->alertLevelAllTraffic();
    if (al < 0) {
        al = 0;
    }
    res.alert_level = al;

    double tmin = std::numeric_limits<double>::infinity();
    for (int ti = 1; ti <= daa->lastTrafficIndex(); ++ti) {
        double t = daa->timeToHorizontalClosestPointOfApproach(ti);
        if (std::isfinite(t) && t >= 0.0 && t < tmin) {
            tmin = t;
        }
    }
    if (std::isfinite(tmin)) {
        res.time_to_violation = static_cast<float>(tmin);
    }

    // Fallback geometry: horizontal vector from ownship to closest traffic in XZ
    double rel_x = 0.0;
    double rel_z = 0.0;
    double best_d2 = std::numeric_limits<double>::infinity();
    for (std::size_t i = 0; i < n; ++i) {
        const double dx = static_cast<double>(traffic_pos[i].x - pos_o.x);
        const double dz = static_cast<double>(traffic_pos[i].z - pos_o.z);
        const double d2 = dx * dx + dz * dz;
        if (d2 < best_d2) {
            best_d2 = d2;
            rel_x = dx;
            rel_z = dz;
        }
    }

    fill_horizontal_bands(daa.get(), res, vel_o.x, vel_o.z, rel_x, rel_z);

    return res;
}

std::unique_ptr<DaidalusWrapper> new_daidalus(const DaidalusCppTune& t) {
    return std::make_unique<DaidalusWrapper>(t);
}
