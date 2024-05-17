#-----------------------------------------------------functions--------------------------------------------------------------------------

#Neighbours(integer-index whose neighbours to find,list- of availables,integer-number of columns):
#function find all neighbours of any particular index in a matrix list a with 'columns' number of columns(default=6 in strands ie 6x8) 
def neighbours(indx,a,columns=6):
    n=[] #initialise the list of neighbours
    #possibilities: total 8 possible neighbours for any number
    # x x  n7  n5  n3 x
    # x x  n1 indx n2 x 
    # x x  n4  n6  n7 x
    #all these possibility's indexes stored in list possibilities(order based on increment/decrement size to reach it,ie n1 and n2 are -+1,while n3 and n4 are -+5 and so on) 
    possible=[(indx-1),(indx+1),(indx-(columns-1)),(indx+(columns-1)),(indx-(columns)),(indx+(columns)),(indx-(columns+1)),(indx+(columns+1))] 
    #contitions stores any special conditions when checking a particular neighbour without which we may get some extra incorrect neighbours in result
    #explanation of each condition pending
    conditions=[int((indx-1)/columns)==int(indx/columns),
                int((indx+1)/columns)==int(indx/columns),
                int((indx-(columns-1))/columns)!=int(indx/columns),
                int((indx+(columns-1))/columns)!=int(indx/columns),
                (indx-(columns))%columns==indx%columns,
                (indx+(columns))%columns==indx%columns,
                int((indx-(columns+1))%columns)<int(indx%columns),
                int((indx+(columns+1))%columns)>int(indx%columns)
                ]
    for i in range(8):#check (1)if each possible neighbour is in list of availables and (2) if special conditions are satisfied
        if((possible[i] in a) and (conditions[i]==True)):
            n.append(possible[i]) #if available and condition satisfied, add to neighbour list
    n.sort() #sord list before returning
    return(n) 


#                            ....................................................................


#index_letter(list- of integer indexes,list of letters(in board))
#function takes list of integer indexes and forms a list of the respective board letters corresponding to each of these letters 
def index_letter(ls,bls):
    lets=[] #initialise list of letters
    for i in ls: #read indexes and appending corresponding letters from letter list
        lets.append(bls[i])
    return(lets)


#                             ....................................................................


#chain_ahead(string- word sequence to look for, list of letters- in board, list of integer indexes- of available letters in board,list- of the chain formed so far if any(default empty list if new chain) )
#This is a recursive function that trys to find a chain of given sequence of charactars and returns the chain sequence if found, and boolean value 'False' of not found
def chain_ahead(w,bls,avble,chn=[]):
    if(chn==[]):    #when we call this funtion for a word,if enters this if since no chain has been formed yet
        for i in avble:    #we start looking for a match for the first letter of the word in our available indexes
            if(bls[i]==w[0]):   #upon finding a match for the first letter, we can start a chain from here
                chn=[i]                    #first, add index of our first letter match to the chain
                tempAvb=[j for j in avble] #create a temporary list of availables removing only our matched first letter index from it
                tempAvb.remove(chn[-1])
                check=chain_ahead(w[1:],bls,tempAvb,chn) #then, start chain and check if we get a match(return chain list) or it is an incorrect chain(false)
                #w[1:] in the above line since first letter already found,we have to find next letter onwards
                if(check==False): #if we get false,implying the proposed chain doesnt make our word
                    chn=[]        #empty out the chain before continuing
                    continue      #start looking for a new match to our first letter in our available list(inchanged since we used tempAvb when removing the chain's elements)
                else:             #if we get a chain as returned value,it means a matching chain has been found for our word
                    return(chn)   #we sucessfully exit function returning the chain found
        return(False)  #if no more available letters match our first letter of the word, then no more matches, so we exit function returning a false
    else:  #when function calls itself during recursion, it enters this else since a chain is being formed
        nbs=neighbours(chn[-1],avble)   #first, we find the possible neighbours of our latest letter added to the chain
        for i in nbs:                   #then,we iterate through each of these possible neighbours
            if(bls[i]==w[0]):               #First check if the neighbour is the right letter
                chn.append(i)               #if it is the right letter, add it to the existing chain as a possible element 
                if(len(w)==1):              #if we have reached the last letter of the word, implies full chain has been formed sucessfully
                    return(chn)             #start returning the formed chain to previous recursive calls,till we reach our first recursive call(in the 'check' line in previous 'ch==[]' if statement )
                else:                   #if we havent formed a sucessful chain addition,then we must continue it
                    tempAvb=[j for j in avble]  #create temporary list of available indexes removing the recently added letter's index from the previous available list
                    tempAvb.remove(chn[-1])
                    check=chain_ahead(w[1:],bls,tempAvb,chn)    #check if the chain leads to a sucessful chain or an unsucessful dead end
                    if(check==False):   #if we get a false, it means the chosen chain path has ended,and in an unsucess
                        chn.pop()       #we pop or remove the last element from our proposed chain,and continue looking for aa new next element from our current chain point
                        continue
                    else:               #not sure if necessary :If we havent reached a chain end, and chain hasnt dead ended, we continue by returning the formed chain so far to the previous chain call 
                        return(chn)     #not sure if necessary :
        return(False) #not sure if necessary(since the return in the first "if(chn==[])" might handle non chain formed return): If chain is unable to form,return

                
#                          ..........................................................................    

                      
#letters(list- of the rows of the board)
#this function gets all the letters of the alphabet that are not on our buard to help reduce size of our possible words directory
#we also return the remaining letters which are in the board incase we want to use that value for some other functionality
def letters(board):
    is_in=[]    #initialise list of letters that ARE IN our board
    not_in=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']    #list of letters NOT IN board(initialised with all letters,removed as we detect them on the board)
    #not_in=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in board:    #iterate through board letters list
        for j in i:     
            if(j not in is_in):    #if the letter is in the 'not_in'
                is_in.append(j)    #remove from not_in list
                not_in.remove(j)   #add to is_in list
    is_in.sort()    #sort list before returning
    return(is_in,not_in)


#                            ...........................................................................


#filter_length(list- of words to be filtered, integer- minimum allowed word length, integer- maximum allowed word length)
#filter function to filter word list based on allowed length
def filter_length(ls,minlen,maxlen):
    temp=[]    #initialise a temporary list to hold words that pass the length filter ie are of acceptable length
    for i in ls:    #iterate through input list of all words
        if(minlen<=len(i) and len(i)<=maxlen):    #apply length condition, if we pass the condition,
            temp.append(i)    #append the 'passed' word to our temporary list
    return(temp)    #return list of words that satisfy the length condition


#                            .................................................................................


#filter_forbidden(list of words- to be filtered, list of letters- that are not on board or 'forbidden' )
#filter function to filter word list based on allowed letters
def filter_forbidden(ls,forb):
    temp=[i for i in ls]    #initialise a temporary list with all words of our input list, we remove unacceptable words as we go
    for i in ls:    #iterate through input list of all words
        for j in forb:    #iterate through the letters of each word
            if(j in i):   #if a forbidden letter is encountered, remove the word from our allowed word list temp
                temp.remove(i)
                break
    return(temp)    #return list of words that satisfy letters condition


#---------------------------------------------------------Main Function/code------------------------------------------------------------
#initialising variables
minlen=4    #minimum length of words if available,0 in not available
minlen+=1   #+1 to account for /n escape seq char at end of each word
maxlen=9    #maximum length of words if available,0 in not available
maxlen+=1   #+1 to account for /n escape seq char at end of each word
available=[i for i in range(48)]    #available charactars initialised to all letters on board(here 0-47 since board is 6x8=48)
board=[
    "JEAVIC",
    "AALOAL",
    "LPOCDR",
    "LEAMOA",
    "AINCGO",
    "NCOLAT",
    "TEIUOA",
    "ROMGTM"
]    #input board as list of rows
board_lst=[]    #list of induvidual letters on board for ease of processing
for i in board: #convert list of rows 'board' to list of inuvidual letters 'board_lst' by extending empty list with iterable string
    board_lst.extend(i)

board_let,board_missing=letters(board)    #call letters function to get list of (1)letters in board 'board_let and (2)letters missing from board 'board_missing'

#Reading word list from file and storing in list
f=open("words.txt",'r')    #open file
lst1=f.readlines()         #readlines stores all words as elements in a list
f.close()                  #close file
lst=[i.upper() for i in lst1]    #convert all words to uppercase for uniformity to process
print(len(lst))                         #Initial number of words
lst=filter_length(lst,minlen,maxlen)    #apply length filter
print(len(lst))                         #print number of words after filtering based on length
lst=filter_forbidden(lst,board_missing) #apply letter filter
print(len(lst))                         #print number of words after filtering based on letters

#main loop
for i in lst:    #start iterating through words in our word list and see if present as a chain in our board
    tmp=[j for j in available]    #create and use temporary available list to prevent original from being changed for incorrect outputs
    res=chain_ahead(i[:-1],board_lst,tmp)    #result contains the chain if word is present on board, or says 'False' if not present
    if(res!=False):                      #if word is present(ie NOT FALSE)
        print(i)                    #print the word to user
        inp=input("valid?:")        #ask user if word is accepted by game
        if(inp=="y" or inp=="Y"):   #enter 'y' or 'Y' if yes, this helps further filter search so dont miss words present, type any other charactars for no
            for j in res:           #if the word is one of the words, update list of available words
                available.remove(j)
    #else just continue