
from gurobipy import *
import numpy as np
import pandas as pd
from Predictor import return_project
from scipy import sparse

def A_opt(df):
    return np.transpose(np.array(df[['D','K','QB','RB','TE','WR','Salary']].copy()))


def c_opt(df):
    return np.array(df.FPPG)

def b_opt():
    return np.transpose(np.array([1, 1, 1, 2, 1, 3, 60,000]))


def opt_lineup():
    cols = 515
    rows = 7
    df = return_project()
    output = []
    A = A_opt(df)
    c = c_opt(df)
    rhs = b_opt()

    model = Model()
    #model.setParam('OutputFlag', False)
    sense = 6 * [GRB.EQUAL] + [GRB.LESS_EQUAL]
    vars = []

    for j in range(cols):
        vars.append(model.addVar(vtype=GRB.BINARY, obj=c[j]))
    model.update()

    for i in xrange(rows):
        start = A.indptr[i]
        end = A.indptr[i+1]
        variables = [vars[j] for j in A.indices[start:end]]
        coeff = A.data[start:end]
        expr = gurobipy.LinExpr(coeff, variables)
        model.addConstr(lhs=expr, sense=sense[i], rhs=rhs[i])

    model.update()
    model.ModelSense = -1
    model.optimize()
    for v in model.getVars():
        output.append(v.x)

    return np.array(output).ravel()
    #return usage / (capacity * tot * 288)