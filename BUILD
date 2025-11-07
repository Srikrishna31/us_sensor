py_binary(
    name = "us_sensor",
    srcs = [
        "main.py",
        "ultrasonic_sensor_objects.py",
    ],
    data = [
        "TEST/10obstacles.txt",
        "TEST/12sensors.txt",
    ],
    main = "main.py",
    deps = [
        "//src:csv_reader",
        "//src:transformation",
        "@pip//numpy",
    ],
)

py_test(
    name = "uss_test",
    srcs = ["test_ultrasonic_sensor.py"],
    main = "test_ultrasonic_sensor.py",
    deps = [
        ":us_sensor",
    ],
)
