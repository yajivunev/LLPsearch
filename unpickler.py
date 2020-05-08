import msgpack
with open('cinfo10.msgpack','rb') as data_file:
    # data_loaded = json.load(data_file)
    cinfo = msgpack.unpack(data_file)

print(len(cinfo))
print(cinfo.keys())
