import matplotlib.pyplot as plt
from pyecharts import Map
from tqdm import tqdm
import random
import xlrd
import os
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）


class NotNumError(ValueError):
    def __init__(self, year, province, industry, type):
        self.year = year
        self.province = province
        self.industry = industry
        self.type = type
        self.message = 'Data in ({},{},{},{}) is NaN'.format(
            self.year, self.province, self.industry, self.type)


class ProvinceNotFoundError(ValueError):
    pass


class TypeNotFoundError(ValueError):
    pass


class TimeNotFoundError(ValueError):
    pass


class IndustryNotFoundError(ValueError):
    pass


class CO2DataSetNotFoundError(FileNotFoundError):
    pass


class CO2Data:
    '''
    '''
    PROVINCE = [
        'Beijing', 'Tianjin', 'Hebei', 'Shanxi', 'InnerMongolia', 'Liaoning',
        'Jilin', 'Heilongjiang', 'Shanghai', 'Jiangsu', 'Zhejiang', 'Anhui',
        'Fujian', 'Jiangxi', 'Shandong', 'Henan', 'Hubei', 'Hunan',
        'Guangdong', 'Guangxi', 'Hainan', 'Chongqing', 'Sichuan', 'Guizhou',
        'Yunnan', 'Shaanxi', 'Gansu', 'Qinghai', 'Ningxia', 'Xinjiang'
    ]
    PROVINCE_CHINESE = [
        '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江',
        '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川',
        '贵州', '云南', '陕西', '甘肃', '青海', '宁夏', '新疆'
    ]
    COLOR = [
        '#FFFFFF',
        '#FFF68F',
        '#FFDEAD',
        '#FFC1C1',
        '#FF7F50',
        '#FF6EB4',
        '#FF3030',
        '#DEB887',
        '#CAFF70',
        '#C71585',
        '#BDB76B',
        '#BBFFFF',
        '#A9A9A9',
        '#9A32CD',
        '#7FFF00',
        '#7B68EE',
        '#778899',
        '#737373',
        '#66CD00',
        '#525252',
        '#4EEE94',
        '#458B00',
        '#388E8E',
        '#333333',
        '#228B22',
        '#1F1F1F',
        '#00FF00',
        '#00CDCD',
        '#008B45',
        '#0000AA',
    ]
    TIME = [
        1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
        2009, 2010, 2011, 2012, 2013, 2014, 2015
    ]
    TYPE = [
        'Raw Coal', 'Cleaned Coal', 'Other Washed Coal', 'Briquettes', 'Coke',
        'Coke Oven Gas', 'Other Gas', 'Other Coking Products', 'Crude Oil',
        'Gasoline', 'Kerosene', 'Diesel Oil', 'Fuel Oil', 'LPG',
        'Refinery Gas', 'Other Petroleum Products', 'Natural Gas', 'Process',
        'Total'
    ]
    INDUSTRY = [
        'Total Consumption',
        'Farming, Forestry, Animal Husbandry, Fishery and Water Conservancy',
        'Coal Mining and Dressing', 'Petroleum and Natural Gas Extraction',
        'Ferrous Metals Mining and Dressing',
        'Nonferrous Metals Mining and Dressing',
        'Nonmetal Minerals Mining and Dressing',
        'Other Minerals Mining and Dressing',
        'Logging and Transport of Wood and Bamboo', 'Food Processing',
        'Food Production', 'Beverage Production', 'Tobacco Processing',
        'Textile Industry', 'Garments and Other Fiber Products',
        'Leather, Furs, Down and Related Products',
        'Timber Processing, Bamboo, Cane, Palm Fiber & Straw Products',
        'Furniture Manufacturing', 'Papermaking and Paper Products',
        'Printing and Record Medium Reproduction',
        'Cultural, Educational and Sports Articles',
        'Petroleum Processing and Coking',
        'Raw Chemical Materials and Chemical Products',
        'Medical and Pharmaceutical Products', 'Chemical Fiber',
        'Rubber Products', 'Plastic Products', 'Nonmetal Mineral Products',
        'Smelting and Pressing of Ferrous Metals',
        'Smelting and Pressing of Nonferrous Metals', 'Metal Products',
        'Ordinary Machinery', 'Equipment for Special Purposes',
        'Transportation Equipment', 'Electric Equipment and Machinery',
        'Electronic and Telecommunications Equipment',
        'Instruments, Meters, Cultural and Office Machinery',
        'Other Manufacturing Industry', 'Scrap and waste',
        'Production and Supply of Electric Power, Steam and Hot Water',
        'Production and Supply of Gas', 'Production and Supply of Tap Water',
        'Construction',
        'Transportation, Storage, Post and Telecommunication Services',
        'Wholesale, Retail Trade and Catering Services', 'Others', 'Urban',
        'Rural'
    ]

    def __check_path(self, path):
        flag = 1
        filelist = next(os.walk(path))[2]
        for i in filelist:
            if 'Province sectoral CO2 emissions ' in i:
                flag = 0
        if flag:
            raise CO2DataSetNotFoundError(
                'CO2 data file not found in this path.')

    def __init__(self, path):
        try:
            self.__check_path(path)
        except CO2DataSetNotFoundError:
            print('CO2 data file not in this path.')
            self.path = ''
            raise CO2DataSetNotFoundError(
                'CO2 data file not found in this path.')
        else:
            self.path = path

    def set_path(self, new_path):
        '''
        '''
        try:
            self.__check_path(new_path)
        except CO2DataSetNotFoundError:
            print('CO2 data file not in this path. Path will not reset.')
        else:
            self.path = new_path
        return None

    def get_path(self):
        '''
        '''
        return self.path


class CO2DataAnalysis(CO2Data):
    '''
    '''
    def __init__(self, path):
        super().__init__(path)

    def __check_input(self, year='', province='', ftype='', industry=''):
        if province not in CO2DataAnalysis.PROVINCE and province != '':
            raise ProvinceNotFoundError(
                'No procince found! Please check your input!')
        if ftype not in CO2DataAnalysis.TYPE and ftype != '':
            raise TypeNotFoundError('No type found! Please check your input!')
        if year not in CO2DataAnalysis.TIME and year != '':
            raise TimeNotFoundError('No year found! Please check your input!')
        if industry not in CO2DataAnalysis.INDUSTRY and industry != '':
            raise IndustryNotFoundError(
                'No industry found! Please check your input!')

    def __check_data(self, data, year, province, industry, ftype):
        if type(data) == str:
            raise NotNumError(year, province, industry, ftype)

    def get_data(self, year, province, industry, ftype):
        '''
        '''
        if type(industry) == str:  # 只传入一个
            industry = [industry]
        if type(ftype) == str:
            ftype = [ftype]
        self.__check_input(year=year, province=province)
        data = xlrd.open_workbook(
            self.path + 'Province sectoral CO2 emissions {}.xlsx'.format(year))
        table = data.sheet_by_name(province)
        cell = 0
        for i in industry:
            for j in ftype:
                self.__check_input(industry=i, ftype=j)
                cell_temp = table.cell_value(
                    CO2DataAnalysis.INDUSTRY.index(i) + 3,
                    CO2DataAnalysis.TYPE.index(j) + 1)
                try:
                    self.__check_data(cell_temp, year, province, i, j)
                except NotNumError as nerr:
                    print(nerr.message)
                    cell_temp = 0
                cell += cell_temp
        return cell

    def get_multiple_data(self, year, province, industry, ftype):
        '''
        '''
        if type(industry) == str:  # 只传入一个
            industry = [industry]
        if type(ftype) == str:
            ftype = [ftype]
        data = xlrd.open_workbook(
            self.path + 'Province sectoral CO2 emissions {}.xlsx'.format(year))
        res = {}
        for k in province:
            self.__check_input(year=year, province=k)
            table = data.sheet_by_name(k)
            cell = 0
            for i in industry:
                for j in ftype:
                    self.__check_input(industry=i, ftype=j)
                    cell_temp = table.cell_value(
                        CO2DataAnalysis.INDUSTRY.index(i) + 3,
                        CO2DataAnalysis.TYPE.index(j) + 1)
                    if type(cell_temp) == str:
                        cell_temp = 0
                        # raise NotNumError(year, province, i, j)
                    else:
                        cell += cell_temp
            res[i] = cell
        return res

    def time_analysis(self,
                      start=1997,
                      end=2015,
                      province='Beijing',
                      industry_list=['Total Consumption'],
                      ftype_list=['Total']):
        '''
        '''
        data = {}
        for i in tqdm(range(start, end + 1)):
            data[i] = self.get_data(year=i,
                                    province=province,
                                    industry=industry_list,
                                    ftype=ftype_list)
        return data

    def area_analysis(self,
                      year=1997,
                      province_list=[],
                      industry_list=['Total Consumption'],
                      ftype_list=['Total']):
        '''
        '''
        if province_list == []:
            province_list = CO2DataAnalysis.PROVINCE
        data = {}
        for i in tqdm(province_list):
            data[i] = self.get_data(year=year,
                                    province=i,
                                    industry=industry_list,
                                    ftype=ftype_list)
        return data

    def complex_analysis_time(self,
                              start=1997,
                              end=2015,
                              province_list=[],
                              industry_list=['Total Consumption'],
                              ftype_list=['Total']):
        '''
        '''
        if province_list == []:
            province_list = CO2DataAnalysis.PROVINCE
        data = {}
        for i in tqdm(range(start, end + 1)):
            data[i] = self.get_multiple_data(year=i,
                                             province=province_list,
                                             industry=industry_list,
                                             ftype=ftype_list)
        return data

    def complex_analysis_area(self,
                              start=1997,
                              end=2015,
                              province_list=[],
                              industry_list=['Total Consumption'],
                              ftype_list=['Total']):
        '''
        '''
        if province_list == []:
            province_list = CO2DataAnalysis.PROVINCE
        data = {}
        for i in tqdm(province_list):
            data[i] = {}
            for j in range(start, end + 1):
                data[i][j] = self.get_data(year=j,
                                           province=i,
                                           industry=industry_list,
                                           ftype=ftype_list)
        return data


class CO2DataVisualize(CO2DataAnalysis):
    '''
    '''
    def __init__(self, path):
        super().__init__(path)

    def time_visualize(self,
                       start=1997,
                       end=2015,
                       province='Beijing',
                       industry_list=['Total Consumption'],
                       ftype_list=['Total']):
        '''
        '''
        data = self.time_analysis(start, end, province, industry_list,
                                  ftype_list)
        x = list(data.keys())
        y = list(data.values())
        plt.plot(x,
                 y,
                 'o-',
                 label='{}地区'.format(province),
                 color=CO2DataVisualize.COLOR[CO2DataVisualize.PROVINCE.index(
                     province)])
        for a, b in zip(x, y):
            plt.text(a, b, b, ha='center', va='bottom')
        plt.legend()
        plt.xlabel('时间')
        plt.ylabel('数值')
        plt.title('{}地区CO2部分排量-时间数据'.format(province))
        plt.xticks(x, list(map(str, x)), rotation=30)
        plt.savefig(r'./img/{}地区CO2部分排量-时间数据.png'.format(province))
        plt.show()

    def area_visualize(self,
                       year=1997,
                       province_list=[],
                       industry_list=['Total Consumption'],
                       ftype_list=['Total']):
        '''
        '''
        data = self.area_analysis(year, province_list, industry_list,
                                  ftype_list)
        data = sorted(data.items(), key=lambda x: x[-1], reverse=True)
        x = [i[0] for i in data]
        y = [i[1] for i in data]
        explode = [0.1] + [0
                           for _ in range(len(x) - 1)]  # 将某一块分割出来，值越大分割出的间隙越大
        plt.pie(
            y,
            explode=explode,
            labels=x,
            colors=CO2DataVisualize.COLOR,
            shadow=False,  # 无阴影设置
            startangle=90,  # 逆时针起始角度设置
            counterclock=False,  # 顺时针
            rotatelabels=True)  # 标签指向轴心
        plt.title('{}年CO2部分排量-地区数据'.format(year))
        plt.savefig(r'./img/{}年CO2部分排量-地区数据.png'.format(year))
        plt.show()

    def area_visualize_map(self,
                           year=1997,
                           province_list=[],
                           industry_list=['Total Consumption'],
                           ftype_list=['Total']):
        '''
        '''
        data = self.area_analysis(year, province_list, industry_list,
                                  ftype_list)
        x = list(data.keys())
        x_c = [
            CO2DataVisualize.PROVINCE_CHINESE[CO2DataVisualize.PROVINCE.index(
                i)] for i in x
        ]
        y = list(data.values())
        map_ = Map('{}年CO2部分排量-地区数据'.format(year),
                   '包含省份:{}'.format(province_list),
                   width=1700,
                   height=1000)
        map_.add("",
                 x_c,
                 y,
                 visual_range=[min(y), max(y)],
                 maptype='china',
                 is_visualmap=True,
                 visual_text_color='#000')
        map_.render(path=r'./data/{}年CO2部分排量-地区数据.html'.format(year))

    def complex_visualize_time(self,
                               start=1997,
                               end=2015,
                               province_list=[],
                               industry_list=['Total Consumption'],
                               ftype_list=['Total']):
        '''
        '''
        data = self.complex_analysis_area(start, end, province_list,
                                          industry_list, ftype_list)
        for i in data.keys():
            x = list(data[i].keys())
            y = list(data[i].values())
            plt.plot(x,
                     y,
                     'o-',
                     label='{}地区'.format(i),
                     color=CO2DataVisualize.COLOR[
                         CO2DataVisualize.PROVINCE.index(i)])
            for a, b in zip(x, y):
                plt.text(a, b, b, ha='right', va='top')
            plt.text(x[-1], y[-1], i, ha='left', va='center')
        plt.xlabel('时间')
        plt.ylabel('数值')
        plt.title('部分地区CO2排量-时间数据')
        plt.xticks(x, list(map(str, x)), rotation=30)
        plt.savefig(r'./img/部分地区CO2排量-时间数据.png')
        plt.show()
        return None

    def complex_visualize_ares(self,
                               start=1997,
                               end=2015,
                               province_list=[],
                               industry_list=['Total Consumption'],
                               ftype_list=['Total'],
                               sorted_by=0):
        '''
        '''
        data = self.complex_analysis_time(start, end, province_list,
                                          industry_list, ftype_list)
        if sorted_by == 0:
            sorted_by = start
        data_sort = sorted(data[sorted_by].items(),
                           key=lambda x: x[-1],
                           reverse=True)
        x = [i[0] for i in data_sort]
        explode = [0.1] + [0
                           for _ in range(len(x) - 1)]  # 将某一块分割出来，值越大分割出的间隙越大

        leng, widt = 0, 0
        lw = 0
        while leng * widt < end - start:
            if lw:
                leng += 1
            else:
                widt += 1
        lw = 0
        for i in data.keys():
            lw += 1
            y = [data[i][j] for j in x]
            plt.subplot(leng, widt, lw)
            plt.pie(
                y,
                explode=explode,
                labels=x,
                colors=CO2DataVisualize.COLOR,
                shadow=False,  # 无阴影设置
                startangle=90,  # 逆时针起始角度设置
                counterclock=False,  # 顺时针
                rotatelabels=True)  # 标签指向轴心
        plt.title('CO2部分排量-地区数据')
        plt.savefig(r'./img/CO2部分排量-地区数据.png')
        plt.show()

    def complex_visualize_ares_map(self,
                                   start=1997,
                                   end=2015,
                                   province_list=[],
                                   industry_list=['Total Consumption'],
                                   ftype_list=['Total']):
        '''
        '''
        data = self.complex_analysis_time(start, end, province_list,
                                          industry_list, ftype_list)
        x = list(data[start].keys())
        x_c = [
            CO2DataVisualize.PROVINCE_CHINESE[CO2DataVisualize.PROVINCE.index(
                i)] for i in x
        ]
        map_ = Map('CO2部分排量-地区数据',
                   '包含省份:{}'.format(province_list),
                   width=1700,
                   height=1000)
        for i in data.keys():
            y = list(data[i].values())
            map_.add("{}年".format(i),
                     x_c,
                     y,
                     visual_range=[min(y), max(y)],
                     maptype='china',
                     is_visualmap=True,
                     visual_text_color='#000')
        map_.render(path=r'./data/CO2部分排量-地区数据.html')


class CO2DataFactory(CO2Data):
    '''
    '''
    PATH = r'./co2_demo/'

    def __init__(self, path='hobee'):
        if path == 'hobee':
            path = CO2DataFactory.PATH
        self.path = path

    def creat_analysis(self):
        '''
        '''
        return CO2DataAnalysis(self.PATH)

    def creat_visualize(self):
        '''
        '''
        return CO2DataVisualize(self.PATH)

    def creat_param(self):
        '''
        '''
        choice = {
            'year': random.choice(CO2DataFactory.TIME),
            'province': random.choice(CO2DataFactory.PROVINCE),
            'industry': random.choice(CO2DataFactory.INDUSTRY),
            'ftype': random.choice(CO2DataFactory.TYPE)
        }
        return choice


class CO2DataTest(CO2Data):
    '''
    '''
    def __init__(self):
        self.factory = CO2DataFactory()
        self.anal = self.factory.creat_analysis()
        self.visu = self.factory.creat_visualize()

    def analysis_test(self):
        '''
        '''
        print()
        print('Time analysis:')
        print(self.anal.time_analysis())
        print()
        print('Area analysis:')
        print(self.anal.area_analysis())
        return None

    def visualize_test(self):
        '''
        '''
        print()
        print('Time visualize:')
        self.visu.time_visualize()
        self.visu.complex_visualize_time()
        print()
        print('Area visualize:')
        self.visu.area_visualize()
        self.visu.complex_visualize_ares()
        print()
        print('Area visualize map:')
        self.visu.area_visualize_map()
        self.visu.complex_visualize_ares_map()
        return None


def main():
    test = CO2DataTest()
    test.analysis_test()
    test.visualize_test()
    return None


if __name__ == '__main__':
    main()
