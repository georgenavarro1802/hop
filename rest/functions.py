def generate_file_name(name, original):
    ext = ""
    if original.find("."):
        ext = original[original.rfind(".")]
        print(ext)
    return "{}.{}".format(name, ext)
