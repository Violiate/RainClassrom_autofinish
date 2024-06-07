import datetime,time
from itertools import combinations
import logging,os
from logging.handlers import TimedRotatingFileHandler
import sys
import requests,json

COOKIE=''   #使用前自行填写cookie和cookie里的csrftoken
csrftoken=''  #自行填写
for i in range(1):
 path=os.getcwd()
 nowdate = datetime.datetime.now()
 filelog = True
 path = path+'/log/'+'log'

 logger = logging.getLogger('log')
 logger.setLevel(logging.DEBUG)

 # 调用模块时,如果错误引用，比如多次调用，每次会添加Handler，造成重复日志，这边每次都移除掉所有的handler，后面在重新添加，可以解决这类问题
 while logger.hasHandlers():
     for i in logger.handlers:
         logger.removeHandler(i)

 # file log
 formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
 if filelog:
     fh = TimedRotatingFileHandler(path,encoding='utf-8', when="midnight", interval=1)

     fh.suffix = "%Y-%m-%d.log"  
     fh.setLevel(logging.DEBUG)
     fh.setFormatter(formatter)
     logger.addHandler(fh)

 # console log
 formatter = logging.Formatter('%(message)s')
 ch = logging.StreamHandler(sys.stdout)
 ch.setLevel(logging.INFO)
 ch.setFormatter(formatter)
 logger.addHandler(ch)

if __name__=='__main__':
   
   #先获取课程信息
   get_lessonlist_headers={
       
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Cookie":COOKIE,
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "university-id": "0",
    "x-client": "web",
    "xt-agent": "web",
    "xtbz": "ykt"
      }
   get_lessonlist_url='https://www.yuketang.cn/v/course_meta/learning_list/'
   get_lessonlist=requests.get(url=get_lessonlist_url,headers=get_lessonlist_headers)
   print("当出现课程是你要刷的，请输入1，否则输入0进行跳过")
   for lesson in get_lessonlist.json()['data']:
      print("\n课程号："+str(lesson['classroom_id'])+"  课程名称："+lesson['course_name']+"  班级："+lesson['classroom_name'])
      select=input("是否跳过？跳过输入0，确认输入1：")
      classroom_id=lesson['classroom_id']
      university_id=lesson['university_id']
      course_id=lesson['course_id']
      
      if(int(select)==1): 
         break
   datetime=int(round(time.time()*1000))
   get_select_lesson_headers={
        
     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "cookie":COOKIE,
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'

       }
   get_select_lesson_url="https://www.yuketang.cn/v/course_meta/classroom_logs?course_id="+str(course_id)+"&classroom_id="+str(classroom_id)+"&activity_type=-1&date_time="+str(datetime)
   get_select_lesson=requests.get(url=get_select_lesson_url,headers=get_select_lesson_headers,allow_redirects=True)
   for activity in get_select_lesson.json()['data']['activities']:
      for number in activity:
          time_struct = time.localtime(number['create_time'])    # 首先把时间戳转换为结构化时间
          time_format = time.strftime("%Y-%m-%d %H-%M-%S",time_struct)   
          print("\n发布时间："+time_format+" 标题："+number['title'])
          select=input("是否跳过？跳过输入0，确认输入1：")
          courseware_id=number['courseware_id']
          id=number['id']
          course_id=lesson['course_id']
      
          if(int(select)==1):
             break
      if(int(select)==1):
         break
   get_select_activity_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'classroom-id': str(classroom_id),
    'cookie': COOKIE,
    'priority': 'u=1, i',
    'referer': get_select_lesson_url,
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'university-id':str(university_id),
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'x-client': 'web, h5',
    'xt-agent': 'h5',
    'xtbz': 'ykt',
} 
   datetime=int(round(time.time()*1000))
   get_select_activity_url='https://www.yuketang.cn/c27/online_courseware/xty/kls/pub_news/'+str(courseware_id)+'/?date_time='+str(datetime)
   get_select_activity=requests.get(headers=get_select_activity_headers,url=get_select_activity_url)
   for content in get_select_activity.json()['data']['content_info']:
      for section in content['section_list']:
         for leaf in section['leaf_list']:
            if int(leaf['leaf_type'])==0:
               leaf_title=leaf['title']
               leaf_id=leaf['id']
               leaf_title=leaf['title']
               print('检测到视频！视频id：'+str(leaf_id)+'标题：'+str(leaf_title))
               get_video_info_url='https://www.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/'+str(classroom_id)+'/'+str(leaf_id)+'/'
               get_video_info_headers = {
                     'accept': 'application/json, text/plain, */*',
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    'classroom-id':str(classroom_id),
                    'cookie': COOKIE,
                    'priority': 'u=1, i',
                    'referer': 'https://www.yuketang.cn/bindmobile/video-student-unit/'+str(classroom_id)+'/'+str(leaf_id),
                    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'university-id': str(university_id),
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
                    'uv-id': str(university_id),
                    'xt-agent': 'web',
                    'xtbz': 'ykt',
                 
                    }
               get_video_info=requests.get(url=get_video_info_url,headers=get_video_info_headers)
               user_id=get_video_info.json()['data']['user_id']
               sku_id=get_video_info.json()['data']['sku_id']
               ccid=get_video_info.json()['data']['content_info']['media']['ccid']
               d = get_video_info.json()['data']['content_info']['media']['duration']
               media_size=get_video_info.json()['data']['content_info']['media']['size']
               get_video_length_headers = {
                  'accept': 'application/json, text/plain, */*',
                  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                  'classroom-id': str(classroom_id),
                  'cookie': COOKIE,
                  'priority': 'u=1, i',
                  'referer': 'https://www.yuketang.cn/bindmobile/video-student-unit/'+str(classroom_id)+'/'+str(leaf_id),
                  'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Windows"',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'same-origin',
                  'university-id': str(university_id),
                  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
                  'uv-id': str(university_id),
                  'xt-agent': 'web',
                  'xtbz': 'ykt',
                        }
               get_video_length_params = {
                  'cid': str(course_id),
                  'user_id': str(user_id),
                  'classroom_id': str(classroom_id),
                  'video_type': 'video',
                  'vtype': 'rate',
                  'video_id': str(leaf_id),
                  'snapshot': '1',
                    }
               get_video_length=requests.get('https://www.yuketang.cn/video-log/get_video_watch_progress/',params=get_video_length_params,headers=get_video_length_headers)
               #video_length=get_video_length.json()['data'][str(leaf_id)]['video_length']
               try:
                sunci = get_video_length.json()['data'][str(leaf_id)]['completed']
               except Exception as e:
                sunci = 0
               while sunci != 1:
                for k in range(25):
                    time.sleep(0.6)
                    print("当前进度：" + str(4 * (k + 1)) + "%")
                    heart_url = 'https://www.yuketang.cn/video-log/heartbeat/'
                    heart_data = '{"heart_data":[{"i":5,"et":"heartbeat","p":"web","n":"ali-cdn.xuetangx.com","lob":"ykt","cp":' + str(d * (1 + k) / 25) + ',"fp":100,"tp":100,"sp":5,"ts":"' + str(datetime + d * (1 + k) * 2500) + '","u":' + str(user_id) + ',"uip":"","c":' + str(course_id) + ',"v":' + str(leaf_id) + ',"skuid":' + str(sku_id) + ',"classroomid":"' +str(classroom_id)+ '","cc":"' + str(ccid)+ '","d":' + str(d) + ',"pg":"' + str(leaf_id) + '_x33v","sq":11,"t":"video","cards_id":0,"slide":0,"v_url":""}]}'

                    heart_headers = {
                          'accept': '*/*',
                          'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                          'classroom-id': str(classroom_id),
                          'content-type': 'application/json',
                          'cookie': COOKIE,
                          'origin': 'https://www.yuketang.cn',
                          'priority': 'u=1, i',
                          'referer': 'https://www.yuketang.cn/bindmobile/video-student-unit/'+str(classroom_id)+'/'+str(leaf_id),
                          'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                          'sec-ch-ua-mobile': '?0',
                          'sec-ch-ua-platform': '"Windows"',
                          'sec-fetch-dest': 'empty',
                          'sec-fetch-mode': 'cors',
                          'sec-fetch-site': 'same-origin',
                          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
                          'x-csrftoken': '',
                          'x-requested-with': 'XMLHttpRequest',
                          'xtbz': 'ykt',
}

                    response = requests.post(url=heart_url, data=heart_data, headers=heart_headers)

                    url = "https://www.yuketang.cn/video-log/get_video_watch_progress/?cid=" + str(course_id) + "&user_id=" + str(user_id) + "&classroom_id=" + str(classroom_id) + "&video_type=video&vtype=rate&video_id=" + str(leaf_id) + "&snapshot=1"
                    response_new = requests.get(url=url, headers=get_video_length_headers)
                    JSON_NEW = json.loads(response_new.text)
                    has_watched = JSON_NEW['data'][str(leaf_id)]['watch_length']
                    if d == 0:
                        d = int(JSON_NEW[str(leaf_id)]['video_length'])
                    

                    try:
                        sunci = JSON_NEW['data'][str(leaf_id)]['completed']
                    except Exception as e:
                        sunci = 0
                    if sunci == 1:
                        break

            elif int(leaf['leaf_type'])==6:    #选择题部分，需要配合无限次提交答案使用
               leaf_id=leaf['id']
               print('选择题部分，需要配合无限次提交答案使用！否则默认提交答案A，结束请输入1 继续输入0：')
               exit_judge=0
               if(exit_judge==1):
                  continue
               get_exercise_info_url='https://www.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/'+str(classroom_id)+'/'+str(leaf_id)+'/'
               get_exercise_info_headers = {
                     'accept': 'application/json, text/plain, */*',
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    'classroom-id':str(classroom_id),
                    'cookie': COOKIE,
                    'priority': 'u=1, i',
                    'referer': 'https://www.yuketang.cn/bindmobile/video-student-unit/'+str(classroom_id)+'/'+str(leaf_id),
                    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'university-id': str(university_id),
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
                    'uv-id': str(university_id),
                    'xt-agent': 'web',
                    'xtbz': 'ykt',
                 
                    } 
               get_exercise_info=requests.get(url=get_exercise_info_url,headers=get_exercise_info_headers)
               user_id=get_exercise_info.json()['data']['user_id']
               sku_id=get_exercise_info.json()['data']['sku_id']
               leaf_type_id=get_exercise_info.json()['data']['content_info']['leaf_type_id']
               get_problems_headers = {
                      'accept': 'application/json, text/plain, */*',
                      'accept-language': 'zh-cn',
                      'classroom-id':str(classroom_id),
                      'cookie': COOKIE,
                      'django-language': 'zh-cn',
                      'platform-id': '0',
                      'priority': 'u=1, i',
                      'referer': get_exercise_info_url,
                      'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                      'sec-ch-ua-mobile': '?0',
                      'sec-ch-ua-platform': '"Windows"',
                      'sec-fetch-dest': 'empty',
                      'sec-fetch-mode': 'cors',
                      'sec-fetch-site': 'same-origin',
                      'university-id': str(university_id),
                      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
                      'x-csrftoken': '',
                      'xtbz': 'ykt',
                          }
               get_problems_url='https://www.yuketang.cn/mooc-api/v1/lms/exercise/get_exercise_list/'+str(leaf_type_id)+'/'+str(sku_id)+'/'+'?term=latest&uv_id='+str(university_id)
               get_problems=requests.get(url=get_problems_url,headers=get_problems_headers)
               for problem in get_problems.json()['data']['problems']:
                  problem_id=problem['problem_id']
                  LibraryID=problem['content']['LibraryID']
                  ProblemID=problem['content']['ProblemID']
                  TemplateID=problem['content']['TemplateID']
                  choose_type=problem['content']['Type']
                  Version=problem['content']['Version']
                  is_correct=False
                  # 待组合的列表
                  lst = ['A', 'B', 'C','D']

                  # 生成所有可能的组合
                  combinations_lst = []
                  for r in range(1, len(lst) + 1):
                     combinations_lst += list(combinations(lst, r))
                  

                  submit_answer_headers = {
                       'accept': 'application/json, text/plain, */*',
                       'accept-language': 'zh-cn',
                       'classroom-id':str(classroom_id),
                       'content-type': 'application/json',
                       'cookie':COOKIE,
                       'django-language': 'zh-cn',
                       'origin': 'https://www.yuketang.cn',
                       'platform-id': '0',
                       'priority': 'u=1, i',
                       'referer': get_problems_url,
                       'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                       'sec-ch-ua-mobile': '?0',
                       'sec-ch-ua-platform': '"Windows"',
                       'sec-fetch-dest': 'empty',
                       'sec-fetch-mode': 'cors',
                       'sec-fetch-site': 'same-origin',
                       'university-id': str(university_id),
                       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
                       'x-csrftoken': csrftoken,
                       'xtbz': 'ykt',
                                }
                  submit_answer_url='https://www.yuketang.cn/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id='+str(university_id)
                  for combination in combinations_lst:
                      submit_answer_json_data = {
                           'classroom_id': int(classroom_id),
                           'problem_id': int(problem_id),
                           'sign': '123456',
                           'answer': list(combination),
                             }  
                      submit_answer=requests.post(url=submit_answer_url,headers=submit_answer_headers,json=submit_answer_json_data)
                      if(str(choose_type)=='MultipleChoice'):
                         print('多选题答案'+str(list(combination))+'正确？ '+str(submit_answer.json()['data']['is_correct'])+'提交时间：'+submit_answer.json()['data']['submit_time'])
                         time.sleep(6)   #不然会请求过快报错
                         if(submit_answer.json()['data']['is_correct']):
                         
                           break
                      else:
                        print('单选答案'+str(list(combination))+'正确？ '+str(submit_answer.json()['data']['is_right'])+'提交时间：'+submit_answer.json()['data']['submit_time'])
                        time.sleep(6)   #不然会请求过快报错
                        if(submit_answer.json()['data']['is_right']):
                         
                          break
                      
                        
         
   
   
   
   



