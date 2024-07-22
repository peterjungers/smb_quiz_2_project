# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Program name:     8-Bit Super Mario Bros. Quiz
# Version:          2.0
# Author:           Peter Jungers
# Date:             January/February 2023 (v.1); Spring/Summer 2024 (v.2)
# Description:      Web app quiz about 8-Bit Super Mario Bros. games
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


from smb_quiz_2 import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
