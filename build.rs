use std::fs;
use std::path::Path;

fn main() {
    let mut build = cxx_build::bridge("src/daidalus/mod.rs");
    build.file("src/daidalus/src/daidalus_bridge.cpp")
         .include("src")
         .include("src/daidalus/vendor/daidalus/C++/include")
         .flag_if_supported("-std=c++14");

    let daidalus_src_dir = "src/daidalus/vendor/daidalus/C++/src";
    if let Ok(entries) = fs::read_dir(daidalus_src_dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.extension().and_then(|e| e.to_str()) == Some("cpp") {
                build.file(path);
            }
        }
    }

    build.compile("daidalus_bridge");
        
    println!("cargo:rerun-if-changed=src/daidalus/mod.rs");
    println!("cargo:rerun-if-changed=src/daidalus/src/daidalus_bridge.cpp");
    println!("cargo:rerun-if-changed=src/daidalus/include/daidalus_bridge.h");
    println!("cargo:rerun-if-changed={}", daidalus_src_dir);
}
