import tables


def generate_groupname_list(faultgroup):
    """
    Generator to get names of all childs in faultgroup
    """
    for node in faultgroup._f_itter_nodes('Group'):
        yield node._v_name


def intersectlists(list1, list2):
    """
    Returns list1 ^ list2 (aka the intersection between the list)
    """
    return list(set(list1).intersection(list2))


def differenclists(list1, list2):
    """
    Returns list1 \ list2 (aka all elements in list 1 that are not in list 2)
    """
    return list(set(list1).difference(list2))


def filter_endstatus_status(faultgroup, interestlist=None):
    """
    Sort all Experiments into reached end point (success) or not (failed).
    """
    success = []
    failed = []
    if interestlist is None:
        interestlist = generate_groupname_list(faultgroup)

    for nodename in interestlist:
        node = faultgroup._f_get_child(nodename)
        if node.faults.attrs.endpoint == 0:
            failed.append(node._v_name)
        else:
            success.append(node._v_name)
    return [success, failed]


def filter_experiment_type(faultgroup, faulttype, interestlist=None):
    """
    Filters for a specific fault target. If interestlist is given only
    experiments in this list will be analysed.
    0 memory fault
    1 instruction fault
    2 register fault
    """
    groupnames = []
    if not isinstance(faulttype, int):
        if "memory" in faulttype:
            faulttype = 0
        elif "instruction" in faulttype:
            faulttype = 1
        elif "register" in faulttype:
            faulttype = 2
        else:
            raise ValueError("Faulttype not known")

    if interestlist is None:
        interestlist = generate_groupname_list(faultgroup)

    for nodename in interestlist:
        node = faultgroup._f_get_child(nodename)
        table = node.faults
        for row in table.iterrows():
            if row['fault_type'] == faulttype:
                groupnames.append(node._v_name)
    return groupnames


def filter_experiment_model(faultgroup, faultmodel, interestlist=None):
    """
    Filter for a specific fault model. If interestlist is given only experiments
    in this list will be analysed.
    0 set 0
    1 set 1
    2 Toggle
    """
    if not isinstance(faultmodel, int):
        if "set0" in faultmodel:
            faultmodel = 0
        elif "set1" in faultmodel:
            faultmodel = 1
        elif "toggle" in faultmodel:
            faultmodel = 2
        else:
            raise ValueError("Faultmodel not understood")
    if interestlist is None:
        interestlist = generate_groupname_list(faultgroup)

    groupnames = []
    for nodename in interestlist:
        node = faultgroup._f_get_child(nodename)
        table = node.faults
        for row in table.iterrows():
            if row['fault_type'] == faultmodel:
                groupnames.append(node._v_name)
    return groupnames


def filter_experiment_faultmask(faultgroup, mask, interestlist=None):
    """
    Filter for a certain fault maks. If interestlist is given only experiments
    in this list will be analysed.
    """
    if interestlist is None:
        interestlist = generate_groupname_list(faultgroup)

    retgroups = []
    for nodename in interestlist:
        node = faultgroup._f_get_child(nodename)
        faulttable = node.faults.read()
        for faultrow in faulttable:
            if faultrow['fault_mask'] == mask:
                retgroups.append(node._v_name)
                break
    return retgroups


def filter_faultaddress_exp(faultgroup, lowaddress, highaddress, interestlist=None):
    """
    Filter for a specific fault address range. If interestlist is given only
    experiments in this list will be analysed
    """
    if interestlist is None:
        interestlist = generate_groupname_list(faultgroup)

    retgroups = []
    for nodename in interestlist:
        node = faultgroup._f_get_child(nodename)
        faulttable = node.faults.read()
        for faultrow in faulttable:
            if (faultrow['fault_address'] >= lowaddress) and (faultrow['fault_address'] <= highaddress):
                retgroups.append(node._v_name)
    return retgroups


def filter_triggercounter_exp(faultgroup, lowcounter, highcounter, interestlist=None):
    """
    Filter for a specific trigger hit counter values. If interestlist is given
    only experiments in this list will be analysed
    """
    if interestlist is None:
        interestlist = generate_groupname_list(faultgroup)

    retgroups = []
    for nodename in interestlist:
        node = faultgroup._f_get_child(nodename)
        faulttable = node.faults.read()
        for faultrow in faulttable:
            if (faultrow['trigger_hitcounter'] >= lowcounter) and (faultrow['trigger_hitcounter'] <= highcounter):
                retgroups.append(node._v_name)
    return retgroups
