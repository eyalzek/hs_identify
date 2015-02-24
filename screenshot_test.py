import screenshot

def main():
    for i in range(3):
        screenshot.get("Chrome", "/home/eyal/%d.bmp" %i)

if __name__ == "__main__":
    main()
