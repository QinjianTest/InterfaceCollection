@server.route('/datacollect', methods=['post'])
def datacollect():
#判断接口的请求方式是GET还是POST,POST传值，GET获取统计
    if request.method == 'POST':
        # 获取请求参数是json格式，返回结果是字典
        #params = request.json
        system = request.values.get('system')
        caseName = request.values.get('caseName')
        requestName = request.values.get('requestName')
        result = request.values.get('result')
        time = request.values.get('time')
        date = request.values.get('date')
        if (len(system)> 0 )&(len(caseName)> 0 )&(len(requestName)> 0 )&(len(result)> 0 )&(len(time)> 0 )&(len(date)> 0 ):      #判断不为空，则写入数据库
            sql_insert = 'insert into data value(%s,%s,%s,%s,%s,%s)'
            insert_database(sql_insert,system,caseName,requestName,result,time,date)
            return jsonify({"code": 200, "mesg": "Data upload resultful."})
        else:
            return jsonify({"code": 400, "mesg": "Incomplete data , please check."})

#写入数据后更新统计表
            sql_update = ("insert into report(System,CaseCount,"
            "RequestCount,Seccess,Fail,Rate,Time,Date)"
            "select a.System,a.CaseCount,b.RequestCount,"
            "(CASE WHEN c.Seccess is NULL THEN 0 ELSE c.Seccess END),"
            "(CASE WHEN d.Fail is NULL THEN 0 ELSE d.Fail END),"
            "c.Seccess/(c.Seccess+d.Fail) as Rate,"
            "e.Time,date_format(a.tDate,'%Y-%m-%d') as Date from "
            "((((select System,count(distinct CaseName) as CaseCount,"
            "date_format(Date,'%Y-%m-%d') as tDate from data group by tDate,System asc) a "
            "left outer join"
            "(select System,count(*) as RequestCount,date_format(Date,'%Y-%m-%d') "
            "as tDate from (select System,casename,date from data group by Date,System,RequestName) a "
            "group by tDate,System asc) b "
            "on a.System=b.System and a.tDate=b.tDate) "
            "left outer join "
            "(select System,count(*) as Seccess,date_format(Date,'%Y-%m-%d') as "
            "tDate from data where Result = 1 group by tDate,System asc) c "
            "on a.System=c.System and a.tDate=c.tDate) "
            "left outer join "
            "(select System,count(*) as Fail,date_format(Date,'%Y-%m-%d') as "
            "tDate from data where Result = 0 group by tDate,System asc) d "
            "on a.System=d.System and a.tDate=d.tDate) "
            "left outer join "
            "(select System,sum(Time) as Time,date_format(Date,'%Y-%m-%d') as "
            "tDate from data group by tDate,System asc) e "
            "on a.System=e.System and a.tDate=e.tDate "
            "group by Date,System asc")
            update_report(sql_update)

@server.route('/datareport', methods=['get'])
def datareport():  #结果展示
    if request.method == 'GET':
        sql_search2 = 'select * from report  WHERE TO_DAYS(NOW()) - TO_DAYS(Date) <= 7 order by Date desc'  #展示7天report
        tmp2 = select_data(sql_search2)
        sql_search3 = 'select sum(CaseCount),sum(RequestCount),sum(Seccess),sum(Fail),ROUND(sum(Seccess)/(sum(Seccess)+sum(Fail))*100,0),sum(Time) from report WHERE TO_DAYS(NOW()) - TO_DAYS(Date) <= 7 '  #展示所有系统的7天内汇总
        tmp3 = select_data(sql_search3)
        return render_template('data_collect_report.html',n=tmp2,m=tmp3) #生成html报告