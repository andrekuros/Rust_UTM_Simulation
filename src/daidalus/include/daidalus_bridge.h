#pragma once
#include <memory>
#include "rust/cxx.h"

// Forward declare C++ type for cxx's generated header
class DaidalusWrapper;

#include "hpm_utm_simulator/src/daidalus/mod.rs.h"

namespace larcfm {
    class Daidalus;
}

class DaidalusWrapper {
private:
    std::unique_ptr<larcfm::Daidalus> daa;
public:
    explicit DaidalusWrapper(const DaidalusCppTune& t);
    ~DaidalusWrapper();
    
    DaidalusResult evaluate_pair(
        const Vec3F& pos_a, const Vec3F& vel_a,
        const Vec3F& pos_b, const Vec3F& vel_b
    );

    /** One ownship + N traffic; bands/alerts consider all traffic together. */
    DaidalusResult evaluate_multi(
        const Vec3F& pos_o, const Vec3F& vel_o,
        rust::Slice<const Vec3F> traffic_pos,
        rust::Slice<const Vec3F> traffic_vel
    );
};

std::unique_ptr<DaidalusWrapper> new_daidalus(const DaidalusCppTune& t);
