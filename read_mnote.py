def mnote_reader(path: str):
    info = {"title": "未命名", "author": "佚名", "bpm": 72, "beat": 4}
    note: list[tuple[int, float]] = []

    read_note = False

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip("\n\r ")
                if read_note:
                    if not line.startswith('['):
                        try:
                            pitch, quantity = int(line.split()[0]), float(line.split()[1])
                            note.append((pitch, quantity))
                            assert 1 <= pitch <= 7
                        except ValueError:
                            pass
                        except AssertionError:
                            pass
                        continue
                    else:
                        read_note = False
                start_pos = line.find('[')
                end_pos = line.find(']')
                key = line[start_pos + 1:end_pos]
                value = line[end_pos + 1:len(line)]
                if key in ["title", "author"]:
                    info[key] = value
                elif key in ["bpm", "beat"]:
                    try:
                        info[key] = int(value)
                    except ValueError:
                        pass
                elif key == "begin":
                    read_note = True
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    except IndexError:
        pass

    return info, note
