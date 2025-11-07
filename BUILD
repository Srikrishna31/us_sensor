py_binary(
    name = "us_sensor",
    srcs = ["ultrasonic_sensor.py"],
    main = "ultrasonic_sensor.py",
    deps = ["@pip//numpy"],
)

py_test(
    name = "uss_test",
    srcs = ["test_ultrasonic_sensor.py"],
    deps = [
        ":us_sensor",
        #        "@pip//pytest",
        "@pip__pytest//:pkg",
    ],
)
