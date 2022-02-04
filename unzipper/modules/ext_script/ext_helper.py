import subprocess
import os

from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton

async def __run_cmds_unzipper(command):
    ext_cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ext_out = ext_cmd.stdout.read()[:-1].decode("utf-8")
    return ext_out

async def _extract_with_7z_helper(path, archive_path, password=None):
    if password:
        command = f"7z x -o{path} -p{password} {archive_path} -y"
    else:
        command = f"7z x -o{path} {archive_path} -y"
    return await __run_cmds_unzipper(command)

async def _extract_with_zstd(path, archive_path):
    command = f"zstd -f --output-dir-flat {path} -d {archive_path}"
    return await __run_cmds_unzipper(command)

async def extr_files(path, archive_path, password=None):
    file_path = os.path.splitext(archive_path)[1]
    if file_path == ".zst":
        os.mkdir(path)
        ex = await _extract_with_zstd(path, archive_path)
        return ex
    else:
        ex = await _extract_with_7z_helper(path, archive_path, password)
        return ex

async def get_files(path):
    path_list = []
    for r, d, f in os.walk(path):
        for file in f:
            path_list.append(os.path.join(r, file))
    return path_list

async def make_keyboard(paths, user_id, chat_id):
    num = 0
    i_kbd = InlineKeyboard(row_width=1)
    data = []
    data.append(
        InlineKeyboardButton(f"Upload All ♻️", f"ext_a|{user_id}|{chat_id}")
    )
    data.append(
        InlineKeyboardButton("Cancel ❌", "cancel_dis")
    )
    for file in paths:
        data.append(
            InlineKeyboardButton(f"{num} - {os.path.basename(file)}".encode("utf-8").decode("utf-8"), f"ext_f|{user_id}|{chat_id}|{num}")
        )
        num += 1
    i_kbd.add(*data)
    return i_kbd


### --- Saved for later --- ###
# async def make_keyboard(paths, user_id, chat_id):
#     num = 0
#     i_kbd = []
#     for file in paths:
#         i_kbd.append(
#             [InlineKeyboardButton(f"{num} - {os.path.basename(file)}", f"ext_f|{user_id}|{chat_id}|{num}")]
#         )
#         num += 1
#     i_kbd.append(
#         [InlineKeyboardButton(f"Upload All ♻️", f"ext_a|{user_id}|{chat_id}")]
#     )
#     i_kbd.append(
#         [InlineKeyboardButton("Cancel ❌", callback_data="cancel_dis")]
#     )
#     return i_kbd
