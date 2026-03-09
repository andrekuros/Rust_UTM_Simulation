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
    DaidalusWrapper();
    ~DaidalusWrapper();
    
    DaidalusResult evaluate_pair(
        const Vec3F& pos_a, const Vec3F& vel_a,
        const Vec3F& pos_b, const Vec3F& vel_b
    );
};

std::unique_ptr<DaidalusWrapper> new_daidalus();
