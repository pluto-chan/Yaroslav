import random
import markovify
#import pickle
def chainus(first_step,input_loc,output_loc): # function to convert 0-1 streams to L-R
    lines = [line.rstrip('\n') for line in open(input_loc)]
    
    file = open(output_loc, "a")
    
    for i in range (len(lines)):
        if(first_step=='R'):
            if(i%2==0):
                lines[i]=lines[i].replace("1","R")
                if(i!=len(lines)-1):
                    temp=list(lines[i+1])
                    temp[lines[i].find('R')]='r'
                    temp=''.join(temp)
                    lines[i+1]=temp
            if(i%2==1):
                lines[i]=lines[i].replace("1","L")
                if(i!=len(lines)-1):
                    temp=list(lines[i+1])
                    temp[lines[i].find('L')]='l'
                    temp=''.join(temp)
                    lines[i+1]=temp
        if(first_step=='L'):
            if(i%2==0):
                lines[i]=lines[i].replace("1","L")
                if(i!=len(lines)-1):
                    temp=list(lines[i+1])
                    temp[lines[i].find('L')]='l'
                    temp=''.join(temp)
                    lines[i+1]=temp
            if(i%2==1):
                lines[i]=lines[i].replace("1","R")
                if(i!=len(lines)-1):
                    temp=list(lines[i+1])
                    temp[lines[i].find('R')]='r'
                    temp=''.join(temp)
                    lines[i+1]=temp 
        file.write(lines[i])
        file.write(' ')
    file.write('\n')    
    file.close()
    
def unchainus(line): # the opposite of the previous function
    first_step=find_first_step(line)
    if(first_step=='R'):
        line=line.replace('R','1',1)
    if(first_step=='L'):
        line=line.replace('L','1',1)
   # for i in range(len(lines)):
      #  temp=lines[i][:4]
      #  if(temp.find('L')==-1):
      #      first_step='R'
      #      lines[i]=lines[i].replace("R","1",1)
      #  if(temp.find('R')==-1):
      #      first_step='L'
      #      lines[i]=lines[i].replace("L","1",1)
    for j in range(len(line)//4):
        if(first_step=='R'):
            if(j%2==0):
                line=line.replace("r","0",1)
                line=line.replace("L","1",1)
            if(j%2==1):
                line=line.replace("l","0",1)
                line=line.replace("R","1",1)
        if(first_step=='L'):
            if(j%2==0):
                line=line.replace("l","0",1)
                line=line.replace("R","1",1)
            if(j%2==1):
                line=line.replace("r","0",1)
                line=line.replace("L","1",1)
    line=line.replace(" ", "\n")
    return line

    
def find_first_step(line):
    temp=line[:4]
    if(temp.find('L')==-1):
        first_step='R'
    if(temp.find('R')==-1):
        first_step='L'
    return first_step

def find_last_step(line,first_step):
    if(((len(line)-line.count(' '))/4)%2==0):
        if(first_step=='R'):
            last_step='L'
        else:
            last_step='R'
    else:
        if(first_step=='R'):
            last_step='R'
        else:
            last_step='L'
    return last_step

def connector(line1,line2,last_step,next_step): # the thing which combines generated streams in a big one
    check1=line1[-4:] # last beat of first part
    check2=line2[:4] # first beat of second part
    last_step_feet_pos=check1.find(last_step)
    if(last_step=='L'):
        prev_step='r'
    else:
        prev_step='l'
    prev_step_feet_pos=check1.find(prev_step)
    next_step_feet_pos=check2.find(next_step)
    #print(check1,check2,last_step_feet_pos,next_step_feet_pos)
    
    connected_line=line1
    
    if (last_step==next_step): # in this case we definetely need something to avoid double-step
        print('govno')
        if(last_step_feet_pos==next_step_feet_pos): # add a step anywhere possible and connect
            print('shit1')
            first_add_list=['0']*4
            first_add_list[last_step_feet_pos]=last_step.lower()
            first_add_set=[0,1,2,3]
            first_add_set.remove(last_step_feet_pos)
            if(last_step=='R' and last_step_feet_pos!=3):
                first_add_set.remove(3)
            if(last_step=='L' and last_step_feet_pos!=0):
                first_add_set.remove(0)
            step=random.choice(first_add_set)
            first_add_list[step]=prev_step.upper()
            to_add=''
            for i in range(len(first_add_list)):
                to_add=to_add+first_add_list[i]
            connected_line= connected_line + ' ' + to_add
        if(check1[next_step_feet_pos]=='0'): # add a step but not on the place where the stream should start
            print('shit2')
            first_add_list=['0']*4
            first_add_list[last_step_feet_pos]=last_step.lower()
            first_add_set=[0,1,2,3]
            first_add_set.remove(last_step_feet_pos)
            if(last_step=='R' and last_step_feet_pos!=3):
                first_add_set.remove(3)
            if(last_step=='L' and last_step_feet_pos!=0):
                first_add_set.remove(0)
            if(last_step=='R' and next_step_feet_pos!=3 and next_step_feet_pos!=last_step_feet_pos):
                first_add_set.remove(next_step_feet_pos)
            if(last_step=='L' and next_step_feet_pos!=0 and next_step_feet_pos!=last_step_feet_pos):
                first_add_set.remove(next_step_feet_pos)
            step=random.choice(first_add_set)
            first_add_list[step]=prev_step.upper()
            to_add=''
            for i in range(len(first_add_list)):
                to_add=to_add+first_add_list[i]
            connected_line= connected_line + ' ' + to_add
        if(next_step_feet_pos==prev_step_feet_pos): # add a step but make sure to remove the leg from the target arrow
            print('shit3')
            first_add_list=['0']*4
            first_add_list[last_step_feet_pos]=last_step.lower()
            first_add_set=[0,1,2,3]
            first_add_set.remove(last_step_feet_pos)
            if(last_step=='R' and last_step_feet_pos!=3):
                first_add_set.remove(3)
            if(last_step=='L' and last_step_feet_pos!=0):
                first_add_set.remove(0)
            if(last_step=='R' and prev_step_feet_pos!=3 and prev_step_feet_pos!=last_step_feet_pos):
                first_add_set.remove(prev_step_feet_pos)
            if(last_step=='L' and prev_step_feet_pos!=0 and prev_step_feet_pos!=last_step_feet_pos):
                first_add_set.remove(prev_step_feet_pos)
            step=random.choice(first_add_set)
            first_add_list[step]=prev_step.upper()
            to_add=''
            for i in range(len(first_add_list)):
                to_add=to_add+first_add_list[i]
            connected_line= connected_line + ' ' + to_add
    else: # here we may be lucky
        print('ne govno')
        if(prev_step_feet_pos==next_step_feet_pos): # lucky - just connect the 2 streams
            print('good1')
        if(check1[next_step_feet_pos]=='0'): # lucky again 
            print('good2')
        if(next_step_feet_pos==last_step_feet_pos): # bad luck
            print('sooka blya')
            # first part - move other leg cause we still don't want double steps
            first_add_list=['0']*4
            first_add_list[last_step_feet_pos]=last_step.lower()
            first_add_set=[0,1,2,3]
            first_add_set.remove(last_step_feet_pos)
            if(last_step=='R' and last_step_feet_pos!=3):
                first_add_set.remove(3)
            if(last_step=='L' and last_step_feet_pos!=0):
                first_add_set.remove(0)
            step=random.choice(first_add_set)
            first_add_list[step]=prev_step.upper()
            to_add=''
            for i in range(len(first_add_list)):
                to_add=to_add+first_add_list[i]
            connected_line= connected_line + ' ' + to_add
            # second part - move the leg away from required arrow
            last_step_feet_pos=to_add.find(prev_step.upper())
            prev_step_feet_pos=to_add.find(last_step.lower())
            second_add_list=['0']*4
            second_add_list[last_step_feet_pos]=prev_step.lower()
            second_add_set=[0,1,2,3]
            second_add_set.remove(last_step_feet_pos)
            if(last_step=='R' and last_step_feet_pos!=0):
                second_add_set.remove(0)
            if(last_step=='L' and last_step_feet_pos!=3):
                second_add_set.remove(3)
            if(last_step=='R' and last_step_feet_pos!=0 and next_step_feet_pos!=last_step_feet_pos):
                second_add_set.remove(next_step_feet_pos)
            if(last_step=='L' and last_step_feet_pos!=3 and next_step_feet_pos!=last_step_feet_pos):
                second_add_set.remove(next_step_feet_pos)
            step=random.choice(second_add_set)
            second_add_list[step]=last_step.upper()
            to_add=''
            for i in range(len(second_add_list)):
                to_add=to_add+second_add_list[i]
            connected_line = connected_line + ' ' + to_add
        
        temp=connected_line[-4:]
        if(temp.find('l')==-1):
            temp2=list(line2)
            temp2[temp.find('L')]='l'
            temp2=''.join(temp2)
            line2=temp2    
        if(temp.find('r')==-1):
            temp2=list(line2)
            temp2[temp.find('R')]='r'
            temp2=''.join(temp2)
            line2=temp2
        connected_line = connected_line + ' ' + line2
    return connected_line

def generator3000(total,tact,text_model):
    #with open('markov_steps.pkl', 'rb') as fid:
    #    text_model = pickle.load(fid)
    lines= ["" for x in range(5)]
    length = [0]*5
    
    #Generate starting streams
    for i in range(5):
        lines[i]=text_model.make_sentence(max_overlap_ratio=0.7, tries=10000)
        length[i]=(len(lines[i])-lines[i].count(' '))/4/tact
        #print(lines[i], '\n')
        
    final_line=lines[0]
    final_length=length[0]
    
    first_step=find_first_step(final_line)
    last_step=find_last_step(final_line,first_step)

    #print(final_line,'\n',lines[1], '\n', final_length,' ',first_step,' ',last_step)
    
    next_step=find_first_step(lines[1])
    
    curr=1
    #print(final_line)
    
    while final_length < total:
        final_line=connector(final_line,lines[curr],last_step,next_step)
        curr=curr+1
        if(curr==5):
            for i in range(5):
                lines[i]=text_model.make_sentence(max_overlap_ratio=0.7, tries=10000)
                length[i]=(len(lines[i])-lines[i].count(' '))/4/tact
                #print(lines[i], '\n')
            curr=0
        last_step=find_last_step(final_line,first_step)
        next_step=find_first_step(lines[curr])
        final_length=(len(final_line)-final_line.count(' '))/4/tact
    
    return final_line[0:(total*tact*5)]