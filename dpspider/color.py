#!/usr/bin/env python
#coding:utf-8

from datetime import datetime

def printText(obj,textColor='',backgroundColor='',style='',logFile=None,color=True,debug=4):
    '''
    :param obj: print object
    :param textColors: default='' <class str|'red','yellow','green','blue','cyan','purple','black','white'>
    :param backgroundColor: default='' <class str|'red','yellow','green','blue','cyan','purple','black','white'>
    :param style: default='' <class str|'bold','underline'>
    :param logFile: default=None <class str>
    :param color: default=True <class bool>
    :param debug: default=4 <class int|0 NONE,1 [Error],2 [Error][WARING],3 [Error][WARING][INFO],4 ALL>
    :function: print obj with|without color,or pass
    '''
    if not isinstance(obj,str):
        obj = str(obj)
    #------------------------------
    if debug == 4:
        pass
    elif debug == 3:
        if not (obj.startswith('[INFO]') or obj.startswith('[WARING]') or obj.startswith('[Error]')):
            obj = None
    elif debug == 2:
        if not (obj.startswith('[WARING]') or obj.startswith('[Error]')):
            obj = None
    elif debug == 1:
        if not (obj.startswith('[Error]')):
            obj = None
    elif debug == 0:
        obj = None
    #------------------------------
    if logFile:
        with open(logFile,'a') as f:
            time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            f.write('%s %s\n'%(time,obj))
    if not logFile:
        if obj:
            if color == False:
                print(obj)
            if color == True:
                textColors={
                    'black'     : '\033[30m',
                    'red'       : '\033[31m',
                    'green'     : '\033[32m',
                    'yellow'    : '\033[33m',
                    'blue'      : '\033[34m',
                    'purple'    : '\033[35m',
                    'cyan'      : '\033[36m',
                    'white'     : '\033[37m',
                }
                backgroundColors={
                    'black'     : '\033[40m',
                    'red'       : '\033[41m',
                    'green'     : '\033[42m',
                    'yellow'    : '\033[43m',
                    'blue'      : '\033[44m',
                    'purple'    : '\033[45m',
                    'cyan'      : '\033[46m',
                    'white'     : '\033[47m',
                }
                styles={
                    'bold'      : '\033[1m',
                    'underline' : '\033[4m',
                }
                if obj.startswith('[INFO]'):
                    textColor,style = textColors['cyan'],styles['bold']
                elif obj.startswith('[WARING]'):
                    textColor,style = textColors['yellow'],styles['bold']
                elif obj.startswith('[Error]'):
                    textColor,style = textColors['red'],styles['bold']
                else:
                    textColor = textColors[textColor] if textColor in textColors else ''
                    backgroundColor = backgroundColors[backgroundColor] if backgroundColor in backgroundColors else ''
                    style = styles[style] if style in styles else ''
                print('%s%s%s%s\033[0m'%(textColor,backgroundColor,style,obj))

def helpLogging():
    '''
    :function: the help of logging.basicConfig
    '''
    A = '''
        logging.basicConfig 函数各参数:
            filename: 日志文件
            filemode: 日志文件权限，默认为 'a'
            level   : 日志级别，默认为 logging.WARNING [DEBUG|INFO|WARNING|ERROR|CRITICAL]
            stream  : 日志的输出流，可以指定输出到 sys.stderr, sys.stdout 或 文件，默认输出到sys.stderr,当stream和filename同时指定时,stream被忽略
            datefmt : 时间格式
            format  : 输出的格式和内容
                %(levelno)s   : 日志级别数值
            *   %(levelname)s : 日志级别名称
                %(pathname)s  : 程序路径,同sys.argv[0]
            *   %(filename)s  : 程序名称
                %(funcName)s  : 函数名称
                %(lineno)d    : 代码行号
            *   %(asctime)s   : 时间
                %(process)d   : 进程ID
                %(thread)d    : 线程ID
                %(threadName)s: 线程名称
            *   %(message)s   : 日志信息
        '''
    B = '''
        import logging

        logging.basicConfig(level = logging.DEBUG,
                            format = '[%(levelname)s %(asctime)s]: %(message)s',
                            datefmt = '%Y/%m/%d %H:%M:%S',
                            filename = '')
        logging.debug('')
        logging.info('')
        logging.warning('')
        logging.error('')
        logging.critical('')
        '''
    printText(A,color=False)
    printText(B,color=False)

if __name__ == '__main__':
    print(help(printText))
    print(help(helpLogging))