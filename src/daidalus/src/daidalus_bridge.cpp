#include "daidalus/include/daidalus_bridge.h"
#include "Daidalus.h"

using namespace larcfm;

DaidalusWrapper::DaidalusWrapper() {
    daa = std::make_unique<Daidalus>();
    daa->set_DO_365B();
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

    res.alert_level = daa->mostSevereAlertLevel(ac_idx);
    res.time_to_violation = (float)daa->timeToHorizontalClosestPointOfApproach(ac_idx);

    if (res.alert_level > 0) {
        for (int i = 0; i < daa->horizontalDirectionBandsLength(); ++i) {
            if (daa->horizontalDirectionRegionAt(i) == BandsRegion::NONE) {
                Interval interval = daa->horizontalDirectionIntervalAt(i, "rad");
                res.min_safe_heading = (float)interval.low;
                res.max_safe_heading = (float)interval.up;
                break;
            }
        }
    }

    return res;
}

std::unique_ptr<DaidalusWrapper> new_daidalus() {
    return std::make_unique<DaidalusWrapper>();
}
