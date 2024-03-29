import numpy as np
import sympy as sp

# add two matrices
def add(A,B):
    return A+B

# subtract two matrices
def sub(A,B):
    return A-B

# def multiply
def multiply(A,B):
    return A@B

# calculate the norm
def Euclidean_norm(x):
    sum = 0
    for i in range(len(x.T)):
        sum += i**2
    return np.sqrt(sum)

# calculate the basis of the vector
def basis(A):
    R_a,_ = sp.Matrix(A).rref()
    R = np.array(R_a)
    rm,rn=R.shape
    am,_ =A.shape
    X=np.zeros(am)
    rank = 0
    for i in range(rm):
        for j in range(rn):
            if (R[i][j]!=0):
                X[i]=1
                rank +=1
                break
    T=[]
    if(rank==0):
        return []
    for i in range(len(X)):
        if X[i]==1:
            T.append(A[:,i])
    return np.array(T).T


# from: https://blog.csdn.net/u012958850/article/details/125284113     
def P1(A, i, j, row=True):            
    if row:
        A[[i,j]]=A[[j,i]]              
    else:
        A[:,[i,j]]=A[:,[j,i]]          
def P2(A,i,k, row=True):				
    if row:
        A[i]=k*A[i]						
    else:
        A[:,i]=k*A[:,i]					
def P3(A,i,j,k,row=True):               
    if row:
        A[j]+=k*A[i]                    
    else:
        A[:,j]+=k*A[:,i]                
def rowLadder(A, m, n):
    rank=0                                     
    zero=m                                     
    i=0                                         
    order=np.array(range(n))                  
    while i<min(m,n) and i<zero:                
        flag=False                             
        index=np.where(abs(A[i:,i])>1e-10)     
        if len(index[0])>0:                     
            rank+=1                            
            flag=True                         
            k=index[0][0]                      
            if k>0:                             
                P1(A,i,i+k)                     
        else:                                   
            index=np.where(abs(A[i,i:n])>1e-10)
            if len(index[0])>0:               
                rank+=1
                flag=True
                k=index[0][0]
                P1(A,i,i+k,row=False)           
                order[[i, k+i]]=order[[k+i, i]] 
        if flag:                               
            P2(A,i,1/A[i,i])
            for t in range(i+1, zero):
                P3(A,i,t,-A[t,i])
            i+=1                               
        else:                                  
            P1(A,i,zero-1)
            zero-=1                           
    return rank, order         
def simplestLadder(A,rank):
    for i in range(rank-1,0,-1):                
        for j in range(i-1, -1,-1):            
            P3(A,i,j,-A[j,i])
             
def mySolve(A,b):
    m,n=A.shape                                     
    b=b.reshape(b.size, 1)                         
    B=np.hstack((A, b))                           
    r, order=rowLadder(B, m, n)                    
    X=np.array([])                                
    index=np.where(abs(B[:,n])>1e-10)              
    nonhomo=index[0].size>0                        
    r1=r                                           
    if nonhomo:                                    
        r1=np.max(index)+1                        
    solvable=(r>=r1)                               
    if solvable:                                   
        simplestLadder(B, r)                       
        X=np.vstack((B[:r,n].reshape(r,1),         
                            np.zeros((n-r,1))))
        if r<n:                                   
            x1=np.vstack((-B[:r,r:n],np.eye(n-r)))
            X=np.hstack((X,x1))
        X=X[order]
    return X

# find null space
def null_space(A):
    am,_=A.shape
    B=np.zeros(am)
    X=mySolve(A,B)
    return np.linalg.matrix_rank(X)

# output two answers
def solve_matrix(A_b):
    A=np.delete(A_b,-1,1)
    a_m,a_n=A.shape
    a_gaussian_result,_ = sp.Matrix(A).rref()
    a_gaussian_result = np.array(a_gaussian_result)
    
    m,n=A_b.shape
    gaussian_result,_ = sp.Matrix(A_b).rref()
    gaussian_result = np.array(gaussian_result)

    freex_id=[]
    for i in range(n-1):
            freex_id.append(i)
    count_basic=0
    
    for i in range(m):
        for j in range(n-1):
            if(gaussian_result[i][j]!=0):
                #pivot,xj is basic variable
                count_basic+=1
                freex_id.remove(j)
                break
    
    _,rank_a=basis(gaussian_result).shape
    _,rank_a_aug=basis(a_gaussian_result).shape

    if(rank_a!=rank_a_aug):
        return None
    elif(rank_a==a_n):
        solution1=np.zeros(a_n)
        for i in range(a_n):
            solution1[i]=gaussian_result[i][-1]
        return solution1
    elif(rank_a<a_n):
        solution1=np.zeros(a_n)
        solution2=np.zeros(a_n)

        if(len(freex_id)==1):
            solution1[freex_id[0]]=1
            solution2[freex_id[0]]=2
            for i in range(m-1,-1,-1):
                for j in range(n-1):
                    if(gaussian_result[i][j]==1):
                        sum=0
                        for k in range(j+1,n-1):
                            sum+=gaussian_result[i][k]
                        solution1[j]=-solution1[freex_id[0]]*sum+gaussian_result[i][-1]
                        solution2[j]=-solution2[freex_id[0]]*sum+gaussian_result[i][-1]
                        break
            result=(solution1,solution2)
            return result
        else:
            solution1[freex_id[-1]]=1
            for i in range(m-1,-1,-1):
                for j in range(n-1):
                    if(gaussian_result[i][j]==1):
                        sum=0
                        for k in range(j+1,n-1):
                            sum+=gaussian_result[i][k]*solution1[k]
                        solution1[j]=-solution1[freex_id[-1]]*sum+gaussian_result[i][-1]
                        break

            solution2[freex_id[-2]]=1
            for i in range(m-1,-1,-1):
                for j in range(n-1):
                    if(gaussian_result[i][j]==1):
                        sum=0
                        for k in range(j+1,n-1):
                            sum+=gaussian_result[i][k]*solution2[k]
                        solution2[j]=-solution1[freex_id[-1]]*sum+gaussian_result[i][-1]
                        break
            result=(solution1,solution2)
            return result
        