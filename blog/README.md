> 在blog功能模块中，需要用到的html页面有：
> create_blog.html, 
> update_blog.html
> delete_blog.html
> blog_list.html
> blog_detail.html


*  *create_blog.html*  
1. 会传给前端*category*数据，表示对分章的分类栏目
2. 需要前端传回用户创建博客文章时提交的的标题*title*、文章内容*body*、文章标签*tags*。

* *update_blog.html*
1. 会传给前端*category*、*title*、*body*、*tags*数据
2. 需要前端传回用户修改文章后新的*category*、*title*、*body*、*tags*

* delete_blog.html
无数据交互

* *blog_list.html*
文章浏览页面，可作为首页
1. 会传给前端*blog*文章数据以供展示
2. 要求前端传回*search*搜寻（暂时提供按标题和作者搜索）
3. 传回*order*排序，可提供按浏览量排序、按创建时间排序
4. 传回*category*，分类导航
5. *tag*，按标签分类

* *blog_detail.html*
文章详细展示页
1. 会传给前端*blog*、*comments*、
  *pre_blog*、*next_blog*
2. 不需要数据传回


