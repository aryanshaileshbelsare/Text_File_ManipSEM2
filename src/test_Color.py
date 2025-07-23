
# demo_color.py

from project_venv import CustomFile

def main():
    print("→ This is normal text")
    # show_info is decorated in red and then resets
    CustomFile("example.txt").show_info()
    print("→ Back to normal again")

if __name__ == "__main__":
    main()
