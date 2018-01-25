import public
import random
import os

# 答案坐标
ANSWER_POINTS = [
    (316, 993),
    (316, 1174),
    (316, 1366),
    (316, 1570),
]

# 自动答题
AUTO_CLICK = False


def run():
    print()
    input('[*] 题目显示后，按回车搜索答案')
    img = public.screenshot()
    question = img.crop((130, 500, 950, 800))
    answers = img.crop((130, 800, 950, 1600))

    question = public.ocr(question)
    answers = public.ocr(answers, join=False)

    if question and answers:
        res = public.baidu_search(question)
        answer_index = best_answer(answers, res)
        if AUTO_CLICK:
            click(*ANSWER_POINTS[answer_index])

    else:
        print('[*] 少年这题靠你自己了！')


def click(x, y):
    cmd = f'adb shell input swipe {x} {y} {x+random.randint(0,3)} {x+random.randint(0,1)}'
    os.system(cmd)


def best_answer(answers, res):
    freq = list(map(res.count, answers))
    print(f'[*] 答案词频：{freq}')
    return freq.index(max(freq))


if __name__ == '__main__':
    while True:
        run()
