#include "daidalus/include/daidalus_bridge.h"
#include "Daidalus.h"
#include <cmath>
#include <limits>

using namespace larcfm;

namespace {

constexpr double kTwoPi = 6.28318530717958647692;

bool finite_heading_rad(double x) {
    return std::isfinite(x) && !std::isnan(x);
}

/** Try hysteresis and raw horizontal-direction resolution for one turn side (right=true). */
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

/** Prefer library preferred side, then the other (each tries hysteresis + raw). */
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
    const Vec3F& pos_b, const Vec3F& vel_b
) {
    DaidalusResult res;
    res.alert_level = 0;
    res.time_to_violation = -1.0f;
    res.min_safe_heading = 0.0f;
    res.max_safe_heading = 0.0f;

    daa->setOwnshipState("A", 
        Position::makeXYZ(pos_a.x, "m", pos_a.y, "m", pos_a.z, "m"), 
        Velocity::makeVxyz(vel_a.x, vel_a.y, "m/s", vel_a.z, "m/s")
    );
    daa->addTrafficState("B", 
        Position::makeXYZ(pos_b.x, "m", pos_b.y, "m", pos_b.z, "m"), 
        Velocity::makeVxyz(vel_b.x, vel_b.y, "m/s", vel_b.z, "m/s")
    );

    int ac_idx = daa->aircraftIndex("B");
    if (ac_idx <= 0) return res;

    // Highest active alert level for this intruder (DO-365B: checks 3→2→1; often 3 when close).
    // NOT mostSevereAlertLevel() (that is the scale maximum, always 3).
    int al = daa->alertLevel(ac_idx);
    if (al < 0) {
        al = 0;
    }
    res.alert_level = al;
    res.time_to_violation = (float)daa->timeToHorizontalClosestPointOfApproach(ac_idx);

    if (res.alert_level > 0) {
        daa->forceHorizontalDirectionBandsComputation();
        // Ownship horizontal track [rad], consistent with Rust bearing_xz (atan2(dx, -dz)).
        const double own_hd = std::atan2(static_cast<double>(vel_a.x), -static_cast<double>(vel_a.z));

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
            // If current track sits in a conflict sector, use a non-degenerate NONE arc (not [0,2π]).
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
            // Full-circle NONE is not actionable guidance; replace with resolution / geometry below.
            double span = static_cast<double>(res.max_safe_heading) - static_cast<double>(res.min_safe_heading);
            if (span >= kTwoPi - 0.02) {
                res.min_safe_heading = 0.0f;
                res.max_safe_heading = 0.0f;
            }
        }
        // If still no band: DAIDALUS resolution (tries both sides; hysteresis + raw), then LOS perpendicular.
        if (res.min_safe_heading == 0.0f && res.max_safe_heading == 0.0f) {
            const double w = 0.35;
            double hres = best_resolution_heading(daa.get());
            if (finite_heading_rad(hres)) {
                apply_narrow_band(&res.min_safe_heading, &res.max_safe_heading, hres, w);
            } else {
                double rel_x = static_cast<double>(pos_b.x - pos_a.x);
                double rel_z = static_cast<double>(pos_b.z - pos_a.z);
                double horiz = std::hypot(rel_x, rel_z);
                if (horiz > 1.0) {
                    // Same xz convention as Rust: atan2(vx, -vz); perpendicular = sidestep from intruder.
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

    return res;
}

std::unique_ptr<DaidalusWrapper> new_daidalus(const DaidalusCppTune& t) {
    return std::make_unique<DaidalusWrapper>(t);
}
