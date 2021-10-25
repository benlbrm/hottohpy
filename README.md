# Project desciption

This library can be used to discuss with HootoH based stove devices

Actually tested and validated with a CMG Drum stove.

To use this library you need to have a wifi capable stove.

# Usage

```shell
$ stove = Hottoh(address="192.168.1.10", port="5001")
$ stove.connect()
$ stove.get_temperature()
```

You can check example.py 
