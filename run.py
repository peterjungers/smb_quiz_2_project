# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Program name:     8-Bit Super Mario Bros. Quiz
# Version:          1.0
# Author:           Peter Jungers
# Date:             March 2024
# Description:      Web app quiz about 8-Bit Super Mario Bros. games
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


from smb_quiz_2 import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
