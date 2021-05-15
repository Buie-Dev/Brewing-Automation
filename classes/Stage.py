from classes.conditions.FromStart import FromStart
from classes.conditions.Heat import Heat
from classes.conditions.Time import Time
from classes.conditions.FlowRate import FlowRate
from classes.conditions.FlowMatch import FlowMatch
from classes.conditions.AfterStage import AfterStage
from classes.conditions.Volume import Volume
from classes.system_control.Plug import Plug
from classes.system_control.Valve import Valve

class Stage:

    started = False
    completed = False


    def set_units(self, units, s_type):
        f = []
        for unit in units:
            for (key, value) in unit.items():
                content = {}
                content['state'] = value
                if s_type == 'valve':
                    
                    f.append(Valve(key, content))
                else:
                    f.append(Plug(key, content)) 
        return f

    def set_conds(self, conds):
        f = []
        
        for cond in conds:
            cond_type = cond['conditionType']
            if cond_type == 'start':
                f.append(FromStart(cond_type))
            elif cond_type == 'time':
                f.append(Time(cond_type, cond['vTime']))
            elif cond_type == 'afterStage':
                f.append(AfterStage(cond_type, cond['stages']))
            elif cond_type == 'temperature':
                if 'changeType' in cond:
                    f.append(Heat(cond_type, cond['vTemp'], cond['sTemp'], cond['changeType']))
                    continue
                f.append(Heat(cond_type, cond['vTemp'], cond['sTemp']))
            elif cond_type == 'flowRate':
                if 'changeType' in cond:
                    f.append(FlowRate(cond_type, cond['vRate'], cond['sRate'], cond['changeType']))
                    continue
                f.append(FlowRate(cond_type, cond['vRate'], cond['sRate']))
            elif cond_type == 'flowMatch':
                f.append(FlowMatch(cond_type, cond['sRate'], cond['s2Rate']))
            elif cond_type == 'volume':
                f.append(Volume(cond_type, cond['vVolume'], cond['pot'], cond['changeType']))

        return f
        
    def __init__(self, content):
        
        self.__id = content['id']
        self.__stage_name = content['stageName']
    
        
        s_cond = content['start']
        f_cond = content['finish']
        m_cond = content['maintain']
        

        self.__start_plugs = self.set_units(s_cond['plugs'], 'plug')
        self.__start_valves = self.set_units(s_cond['valves'], 'valve')
        self.__start_conds = self.set_conds(s_cond['details'])
  

        self.__finish_plugs = self.set_units(f_cond['plugs'], 'plug')
        self.__finish_valves = self.set_units(f_cond['valves'], 'valve')
        self.__finish_conds = self.set_conds(f_cond['details'])

        self.__maintain_plugs = self.set_units(m_cond['plugs'], 'plug')
        self.__maintain_valves = self.set_units(m_cond['valves'], 'valve')
        self.__maintain_conds = self.set_conds(m_cond['details'])
        

    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__stage_name
    
    def get_start_plugs(self):
        return self.__start_plugs
    
    def get_start_valves(self):
        return self.__start_valves

    def get_start_conds(self):
        return self.__start_conds
    
    def get_finish_plugs(self):
        return self.__finish_plugs
    
    def get_finish_valves(self):
        return self.__finish_valves

    def get_finish_conds(self):
        return self.__finish_conds
    
    def get_maintain_plugs(self):
        return self.__maintain_plugs
    
    def get_maintain_valves(self):
        return self.__maintain_valves

    def get_maintain_conds(self):
        return self.__maintain_conds

    def __str__(self):
        
        s = 'ID: {}'.format(self.get_id())
        s += '\nName: {}'.format(self.get_name())
        s += '\nStart Plugs Size: {}'.format(len(self.get_start_plugs()))
        s += '\nStart Valves Size: {}'.format(len(self.get_start_valves()))
        s += '\nStart Details Size: {}'.format(len(self.get_start_conds()))
        return s
