def CheckRepeatedIDS(id, ids_received):
    
    if ids_received.index(id)==0:
        return True
    else:
        return False
