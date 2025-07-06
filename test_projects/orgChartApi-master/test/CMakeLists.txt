cmake_minimum_required(VERSION 3.5)
project(org_chart_test CXX)

add_executable(${PROJECT_NAME} test_main.cc test_controllers.cc)

target_link_libraries(${PROJECT_NAME} PRIVATE drogon)

ParseAndAddDrogonTests(${PROJECT_NAME})

# Add coverage flags for gcov
set(COVERAGE_COMPILE_FLAGS "-fprofile-arcs -ftest-coverage")
set(COVERAGE_LINK_FLAGS    "-fprofile-arcs -ftest-coverage")

set_target_properties(${PROJECT_NAME} PROPERTIES
    COMPILE_FLAGS "${COVERAGE_COMPILE_FLAGS}"
    LINK_FLAGS    "${COVERAGE_LINK_FLAGS}"
)
