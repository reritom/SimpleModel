from protected_list import ProtectedList

this_list = ProtectedList.of(str)()
this_list.append("Hello")
this_list.insert(0, "New")
this_list.extend(["World, Again"])
