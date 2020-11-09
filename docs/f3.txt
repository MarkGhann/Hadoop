import os as osy
import subprocess as sub
import random as rand
import anopoi as apo
import genclasses as gec
import xml.dom.minidom as xm

souls = dict()
def NOD(a,b):
    while b:
        a, b = b, a % b
    return a

def ocr(dig):
    a = "" +'"'
    a += str(dig)
    return a + '"'

def create_sys(G,name):
    f = open(name,'w')
    f.write("<system>\n")
    start = 0
    stop = 2000000
    task = G.get_task(0)
    stop = task.maj_fr
    for i in range(len(G.Cores)):
        f.write('\t<module major_frame='+ocr(stop)+' name="Module'+str(i)+'">\n')
        f.write('\t\t<partition id="0" name="m0_part0"  scheduler="FPPS">\n')
        for j in G.get_tasks_proc(i):
            task = G.get_task(j)
            f.write('\t\t\t<task id='+ocr(task.index)+' name="task'+str(task.index)+'" wcet='+ocr(task.exac)+' prio='+ocr(task.priority)+' offset="0" period='+ocr(task.per)+' deadline='+ocr(task.deadline)+'/>\n')
        f.write("\t\t</partition>\n")
        f.write('\t\t<window start='+ocr(start)+' stop='+ocr(stop)+' partition="0"/>\n')
        f.write("\t</module>\n")
    for j in G.mass:
        f.write('\t<link src='+ocr(j.src)+' dst='+ocr(j.dst)+' delay='+ocr(j.dly)+'/>\n')
    f.write("</system>\n")
    f.close()
    return None

def use(name1,name2):
    sub.call("./compute.sh")
    return None

#Help(Others)
def wcrtH(G,name,task1,dom):
    tasks = dom.getElementsByTagName("task")
    WCRT = 0
    number = 0
    for t in tasks:
        task = int(t.getAttribute("id"))
        if task != task1:
            period = G.get_task(task).per
            for child in t.getElementsByTagName("job"):
                beg = child.getElementsByTagName("event")[0]
                end = child.getElementsByTagName("event")[-1]
                if end.getAttribute("type") != "finished":
                    print("Others, No finish task: ",task," job:",number+1)
                    #input()
                    return 0
                if not beg:
                    print("Others, there's no task: ",task," job:",number)
                    #input()
                    return 0
                start = number*period
                stop = int(end.getAttribute("time"))
                tmp = stop - start
                if tmp == 0:
                    print("Others, WCRT ZERRO task: ",task," job:",number)
                    #input()
                    return 0
                if tmp == period:
                    flag = False
                    sh = 0
                    summa = 0
                    for s in child.getElementsByTagName("event"):
                        if s.getAttribute("type") == "exec" and not flag:
                            sh = int(s.getAttribute("time"))
                            flag = True
                        elif s.getAttribute("type") == "exec" and flag:
                            print("s.getAttribute(type) == exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                        if (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and flag:
                            sh = int(s.getAttribute("time")) - sh
                            summa += sh
                            flag = False
                        elif (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and not flag:
                            print("s.getAttribute(type) != exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                    if summa != G.get_task(task).exac:
                        print("WCRT == period, but exec' summa != task.exec. Task: ", task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                        #input()
                        return 0
                if tmp > WCRT:
                    WCRT = tmp
                number += 1
            break
    if number == 0:
        print(" the number of jobs == 0 ! in the main cycle task: ",task)
    return WCRT

#Main
def wcrt(G,name,task):
    f = open(name,'r')
    dom = xm.parse(name)
    dom.normalize()
    tasks = dom.getElementsByTagName("task")
    WCRT = 0
    tmpH = wcrtH(G,name,task,dom)
    if tmpH == 0:
        return 0
    period = G.get_task(task).per
    number = 0 #the number of a job
    for t in tasks:
        if int(t.getAttribute("id")) == task:
            for child in t.getElementsByTagName("job"):
                beg = child.getElementsByTagName("event")[0]
                end = child.getElementsByTagName("event")[-1]
                if end.getAttribute("type") != "finished":
                    print("Main, No finish task: ",task," job:",number)
                    #input()
                    return 0
                if not beg:
                    print("Main, there's no task: ",task," job:",number)
                    #input()
                    return 0
                start = number*period
                stop = int(end.getAttribute("time"))
                tmp = stop - start
                if tmp == 0:
                    print("bd wcrt in the main cycle ",tmp)
                    return 0
                if tmp == period:
                    flag = False
                    sh = 0
                    summa = 0
                    for s in child.getElementsByTagName("event"):
                        if s.getAttribute("type") == "exec" and not flag:
                            sh = int(s.getAttribute("time"))
                            flag = True
                        elif s.getAttribute("type") == "exec" and flag:
                            print("s.getAttribute(type) == exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                        if (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and flag:
                            sh = int(s.getAttribute("time")) - sh
                            summa += sh
                            flag = False
                        elif (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and not flag:
                            print("s.getAttribute(type) != exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                    if summa != G.get_task(task).exac:
                        print("WCRT == period, but exec' summa != task.exec. Task: ", task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                        #input()
                        return 0
                if tmp > WCRT:
                    WCRT = tmp
                number += 1
            break
    if number == 0:
        print(" the enumber of jobs == 0 ! in the main cycle task: ",task)
    return WCRT

def comput_wcrt(F,task,name1,name2):
    create_sys(F,name1)
    use(name1,name2)
    fa = wcrt(F,name2,task)
    print("-----------------------------------> ",fa)
    return fa

def ifitness(list1,G,task,nameinp,nameout,co):
    co += 1
    F = dict()
    keys = list1.keys()
    for i in G.Tree.keys():
        if i in keys:
            G.Tree[i].exac = list1[i]
            print(i, "     ", list1[i])
        else:
            G.Tree[i].exac = G.get_task(i).timeinterval[1]
    return comput_wcrt(G,task,nameinp,nameout),co

def prob(a = 0, b = 10):
    return rand.randint(a,b)

def unio(list1,list2):
    for i in range(len(list2)):
        list1 += [list2[i]]
    return list1

def crossing(list1,list2,a):
    chd1 = list1.copy()
    chd2 = list2.copy()
    count = 0
    for i in list2.keys():
        if count <= a:
            count += 1
        else:
            chd1[i] = list2[i]
    count = 0
    for i in list1.keys():
        if count <= a:
            count += 1
        else:
            chd2[i] = list1[i]
    return gec.Ind(chd1,0), gec.Ind(chd2,0)

def mutating(G,list1,vol,task):
    hm = int((len(list1.keys())/100)*vol)
    count = 0
    for i in list1.keys():
        if count == hm:
            break
        if prob(0,1):
            continue
        list1[i] = prob(G.get_task(i).timeinterval[0],G.get_task(i).timeinterval[1])
    return list1

def best(matr,vol):
    hm = vol
    matr2 = []
    matr = sorted(matr,key=lambda elem: elem.fitness,reverse=True)
    for i in range(hm):
        matr2 += [matr[i]]
    return matr2

def worst(matr,vol):
    hm = vol
    matr2 = []
    matr = sorted(matr,key=lambda elem: elem.fitness)
    for i in range(hm):
        matr2 += [matr[i]]
    return matr2
        
def same(set1 = set(), set2 = set()):
    pass

def putvals(set1 = set()):
    vals = []
    for i in range(len(set1)):
        vals += [i]
    return sorted(vals)

def initial_pop(G,task,nameinp,nameout,co):
    pop = []
    anomals = G.get_task(task).anomal
    vals = dict()
    pp = []
    for k in anomals: 
        vals[k] = G.get_task(k).timeinterval[1]
    for y in sorted(vals.keys()):
        pp += [vals[y]]
    tpp = tuple(pp)
    if tpp in souls.keys():
        pass
    else:
        aq,co =  ifitness(vals,G,task,nameinp,nameout,co)
        if aq == 0:
            return vals,-1
        souls[tpp] = aq
    pop += [gec.Ind(vals, souls[tpp])]
    for i in range(25):
        vals = dict()
        pp = []
        for k in anomals: 
            vals[k] = apo.get_time_p_A(G.get_task(k))
        for y in sorted(vals.keys()):
            pp += [vals[y]]
        tpp = tuple(pp)
        if tpp in souls.keys():
            pass #print("It was before!")
        else:
            aq,co =  ifitness(vals,G,task,nameinp,nameout,co)
            if aq == 0:
                return vals,-1
            souls[tpp] = aq
        pop += [gec.Ind(vals, souls[tpp])]
    return pop,co

def fitness(matr,G,T):
    if not matr:
        return -1, None
    WCRT = -1
    j = -1
    for i in range(len(matr)):
        if matr[i].fitness > WCRT:
            WCRT = matr[i].fitness
            j = i
    return WCRT, matr[j]

def cross(matr):
    childs = []
    size = len(matr)-1
    for i in range((size+1)//2):
        j = prob(0,size)
        k = prob(0,size)
        a = prob(0,len(matr[j].vals))
        child1, child2 = crossing(matr[j].vals,matr[k].vals,a)
        childs += [child1] + [child2]
    #childs = same(childs,matr)
    return childs

def mutation(G,matr,task):
    for i in range(len(matr)):
        pr = prob(0,100)
        if pr <= 50:
            continue
        #input()
        matr[i].vals = mutating(G,matr[i].vals,matr[i].mutval,task)
        #input()
    #matr = same(matr)
    return matr

def selection(matr,G,task,nameinp,nameout,co):
    BADWCRT = False
    for i in range(len(matr)):
        pp = []
        for y in sorted(matr[i].vals.keys()):
            pp += [matr[i].vals[y]]
        tpp = tuple(pp)
        if tpp in souls.keys():
            pass #print("It was before!")
        else:
            aq,co = ifitness(matr[i].vals,G,task,nameinp,nameout,co)
            #print(aq)
            if aq == 0:
                return matr[i].vals, -1
            souls[tpp] = aq
        matr[i].fitness = souls[tpp]
    for i in range(len(matr)):
        if matr[i].fitness <= 0:
            print("bad select! ",matr[i].fitness)
    matr1 = best(matr,23)
    matr2 = worst(matr,3)
    return unio(matr1,matr2),co

def turn(vals,f,G):
    l = len(vals)
    end = False
    j = 0
    for i in sorted(vals.keys()):
        ll = G.get_task(i).timeinterval[1] - G.get_task(i).timeinterval[0] + 1
        if f[j] >= ll:
            if j == l-1:
                end = True
                break
            f[j+1] += 1
            f[j] = 0
        vals[i] = G.get_task(i).timeinterval[0] + f[j]
        #print(G.get_task(i).timeinterval[0])
        if j == 0:
            f[j] += 1
        j += 1
    return vals,f,end

def BF(G,task,nameinp,nameout,anomal):
    vals = dict()
    if not anomal:
        #input()
        print("No anomals")
        return 0,0
    f = [0 for k in range(len(anomal))]
    for i in anomal:
        vals[i] = 0
    WCRT = -1
    end = False
    count = 0
    co = 0
    while not end:
        #print("Brute forse<<<<<<<<<<<<<<<<<<<<<<")
        count += 1
        #print(count)
        vals,f,end = turn(vals,f,G)
        #print(vals.values())
        #input()
        tmp,co = ifitness(vals,G,task,nameinp,nameout,co)
        if tmp > WCRT:
            WCRT = tmp
    return WCRT,count

def genetic(G,task,nameinp,nameout):
    count = 1
    #print("IN>")
    #input()
    co = 0
    pop,co = initial_pop(G,task,nameinp,nameout,co)
    if co == -1:
        return 0, pop,co
    #print("OUT>")
    #input()
    #for i in range(len(pop)):
    #    print(pop[i].vals)
    if not pop:
        print("Sth is going wrong, a population is empty.")
        return 0,None
    maxWCRT, searchind = fitness(pop,G,task)
    while count < 10:
        pop_c = cross(pop)
        pop_c = mutation(G,pop_c,task)
        pop = unio(pop,pop_c)
        pop,co = selection(pop,G,task,nameinp,nameout,co)
        if co == -1:
            return 0, pop,co
        WCRT, ind = fitness(pop,G,task)
        if maxWCRT < WCRT:
            count = 1
            maxWCRT = WCRT
            searchind = ind
        else:
            count += 1
    else:
        pass #print("No while")
    if not searchind:
        return -1, None
    return maxWCRT, searchind.vals,co
