import argparse
import os
import sys
import subprocess
import traceback

VER = 'v0.2'
desc = '把视频分割为两半  by 谢耳朵 ' + VER

BASE = os.path.dirname(__file__ if not hasattr(sys, 'frozen') else sys.executable)
os.chdir(BASE)
ffprobe = 'ffprobe'
ffmpeg = 'ffmpeg'

def initparser():
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('input', help='待分割视频')
    parser.add_argument('-q', '--quit', action='store_true', help='结束后不暂停程序直接退出，方便命令行调用。不加该参数程序结束时会暂停。')
    return parser

def mkOutfilenames(infile: str):
    infile = os.path.abspath(infile)
    path, suf = os.path.splitext(infile)
    dirname, name = os.path.split(path)
    out1 = os.path.join(dirname, name+'_1'+suf)
    out2 = os.path.join(dirname, name+'_2'+suf)
    return out1, out2

def getLength(infile: str) -> float:
    '''return secs in float'''
    # def t2s(t):
    #     h, m, s = t.strip().split(":")
    #     return int(h) * 3600 + int(m) * 60 + int(s)
    out = subprocess.check_output([ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', infile]).decode('utf8')
    #! 就算文件不存在返回码也是0，但输出为空
    if out:
        return float(out.strip())
    return -1

    # res = re.search(r'Duration: ([\d:]+)', out)
    # if not res or not res[1]:
    #     raise Exception('\n错误：获取视频时长失败，正则匹配错误！')
    # duration = res[1]  # 00:25:25
    # secs = t2s(duration)
    # return secs

def dosplit(first, mid, infile, outfile):
    if first:
        res = subprocess.run(["ffmpeg", '-t', str(mid), '-i', infile, '-c', 'copy', '-y', outfile], capture_output=True)
    else:
        res = subprocess.run(["ffmpeg", '-ss', str(mid), '-i', infile, '-c', 'copy', '-y', outfile], capture_output=True)
    #! 就算正常运行 输出也在stderr里
    if res.returncode != 0:
        print(res.stderr.decode('utf8'))
        print('错误：切割失败，请检查报错信息！')
        return False
    return True

def splitVideo(infile: str):
    try:
        secs = getLength(infile)
        assert secs >= 0
        print('视频时长', secs, '秒')
    except (AssertionError, Exception):
        raise Exception('\n错误：获取视频时长失败！')

    mid = secs//2
    outfile1, outfile2 = mkOutfilenames(infile)

    print('\n切分前半部分...')
    #print(cmd)
    res = dosplit(True, mid, infile, outfile1)  # first half
    if not res: return '', ''

    print('\n切分后半部分...')
    res = dosplit(False, mid, infile, outfile2)  # second half
    # subprocess.check_output([*cmd.split(' ')])
    if not res: return '', ''

    return outfile1, outfile2

def main():
    parser = initparser()
    args = parser.parse_args()
    try:
        out1, out2 = splitVideo(args.input)
        if out1 and out2:
            print('\n成功！已输出至', out1, out2, sep='\n')
    except Exception as err:
        print('\n发生未预料错误！\n')
        traceback.print_exc()
    finally:
        if not args.quit:
            print()
            os.system('pause')

if __name__ == '__main__':
    main()