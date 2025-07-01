# 数据分析与可视化学习总结  
## 2025年7月1日  


### 一、学习内容概述  
今日学习围绕Python数据分析与可视化展开，通过多个实战案例掌握了以下核心技能：  
1. **数据读取与预处理**：使用pandas读取CSV文件，处理缺失值（`dropna`）、数据类型转换（`pd.to_numeric`）。  
2. **分组统计与交叉分析**：利用`groupby`和`pivot_table`进行多维度数据聚合（如性别、年龄、乘客等级对生还率的影响）。  
3. **可视化图表绘制**：使用matplotlib和seaborn创建柱状图、直方图、热力图，优化图表样式（颜色、标签、网格线等）。  
4. **中文字体与图表优化**：解决中文显示问题，设置DPI、字体样式，添加统计量（均值、中位数）标注。  


### 二、重点知识点总结  

#### 1. 数据处理核心操作  
- **分组统计**：通过`groupby`按类别（如`Sex`、`Pclass`）分组，计算生还率均值：  
  ```python
  survival_by_sex = df.groupby('Sex')['Survived'].mean().reset_index()
  ```  

- **数据分箱**：使用`pd.cut`将连续变量（年龄）离散化，便于分组分析：  
  ```python
  age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
  df['年龄组'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)
  ```  

- **交叉表与透视表**：通过`pivot_table`生成多维度交叉表，如年龄-性别生还率矩阵：  
  ```python
  pivot_data = survival_by_age_sex.pivot(index='年龄组', columns='Sex', values='Survived')
  ```  

#### 2. 可视化图表实战  
- **分组柱状图**：用于对比不同类别或交叉类别的数值差异（如男女在各年龄组的生还率）：  
  ```python
  x = np.arange(len(age_groups))
  plt.bar(x - width/2, male_survival, width, label='男性')
  plt.bar(x + width/2, female_survival, width, label='女性')
  ```  

- **直方图**：展示连续变量的分布（如生还者年龄分布），可添加均值、中位数参考线：  
  ```python
  plt.hist(survived_ages, bins=20, color='#00A1FF')
  plt.axvline(survived_ages.mean(), color='red', linestyle='dashed', label=f'平均值: {mean:.1f}')
  ```  

- **热力图**：直观展示二维矩阵数据的相关性或分布（年龄-性别生还率交叉表）：  
  ```python
  import seaborn as sns
  sns.heatmap(pivot_data, annot=True, fmt=".2%", cmap="YlGnBu")
  ```  

#### 3. 图表优化与细节处理  
- **中文字体设置**：通过`plt.rcParams['font.sans-serif']`指定中文字体（如`SimHei`），确保中文正常显示：  
  ```python
  plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
  ```  

- **数值标签与格式**：在柱状图上方添加百分比或具体数值，提升图表可读性：  
  ```python
  for bar in bars:
      height = bar.get_height()
      plt.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{height:.2%}', ha='center')
  ```  

- **图表样式优化**：去除冗余边框，添加网格线，调整颜色与布局：  
  ```python
  plt.gca().spines['top'].set_visible(False)  # 隐藏上边框
  plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加纵向网格线
  plt.tight_layout()  # 自动调整布局
  ```  


### 三、实战案例总结  
#### 1. 泰坦尼克号生还率分析  
- **单变量分析**：性别、年龄组、乘客等级对生还率的影响，发现女性生还率显著高于男性，儿童（0-10岁）生还率最高。  
- **多变量交叉分析**：通过分组柱状图和热力图，直观展示年龄与性别的交互作用，如女性在各年龄组的生还率均高于男性。  

#### 2. 奖牌数量对比与GDP分布  
- 使用分组柱状图对比各国金、银、铜牌数量，通过直方图分析GDP数据的集中趋势与离散程度（均值、标准差）。  


### 四、遇到的问题与解决方法  
#### 1. 中文字体显示异常  
- **问题**：图表中文字体显示为方块或乱码。  
- **解决**：明确指定系统中文字体（如`SimHei`），或通过字体文件路径加载字体。  

#### 2. 数据合并与缺失值处理  
- **问题**：多文件合并时遇到列名不一致或缺失值。  
- **解决**：使用`pd.concat`合并数据，通过`dropna`或`fillna`处理缺失值，确保分析数据完整。  

#### 3. 图表布局混乱  
- **问题**：多子图或标签重叠导致图表不清晰。  
- **解决**：使用`plt.tight_layout()`自动调整布局，或手动设置`figsize`和边距。  


### 五、学习体会与未来计划  
#### 体会  
1. 数据可视化是传达数据分析结论的关键，不同图表类型（柱状图、直方图、热力图）适用于不同场景。  
2. 数据预处理（清洗、分箱、转换）占分析流程的大部分时间，直接影响分析结果的准确性。  
3. 代码模块化（如将绘图逻辑封装为函数）可提高开发效率，便于维护。  

#### 未来计划  
1. 学习更多可视化库（如pyecharts），尝试交互式图表。  
2. 深入学习统计分析方法（如假设检验、相关性分析），结合可视化提升数据分析深度。  
3. 挑战复杂数据集（如时间序列、文本数据），拓展数据处理技能。  


### 六、代码复用与优化建议  
- 将常用功能封装为函数（如`load_data()`、`plot_survival()`），减少重复代码。  
- 增加数据验证逻辑（如检查列是否存在、数据类型是否正确），提升代码鲁棒性。  
- 使用`seaborn`等高级库简化可视化流程，同时保持图表美观性。