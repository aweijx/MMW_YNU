//index.js
//获取应用实例
const app = getApp()
var util = require('../../utils/util.js');

Page({
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '搜索', //导航栏 中间的标题
      height: 0
    },
    date: "",
    skip:0,//第几次加载
    picker_data: [],
    picker_index: [],
    listData:[
      {
        name:'失物招领',
        id:1,
        children:[
          {
            name:'物品类别',
            id:11,
            children:[
              {
                name:'钱包',
                id:111
              },
              {
                name:'钥匙',
                id:112
              },
              {
                name:'宠物',
                id:113
              },
              {
                name:'卡类/证照',
                id:114
              },
              {
                name:'数码产品',
                id:115
              },
              {
                name:'书籍/文件',
                id:116
              },
              {
                name:'衣服/鞋帽',
                id:117
              },
              {
                name:'首饰/挂饰',
                id:118
              },
              {
                name:'行李/包裹',
                id:119
              },
              {
                name:'手袋/挎包',
                id:1110
              },
              {
                name:'其它',
                id:1111
              },
            ]
          },
          {
            name:'物品名称',
            id:12,
            children:[
              {
                name:'请填写想要查找的物品名',
                id:121
              },
            ]
          },
          {
            name:'日期',
            id:13,
            children:[
              {
                name:'06-11',
                id:131
              },
              {
                name:'06-12',
                id:132
              },
              {
                name:'06-13',
                id:133
              },
              {
                name:'06-14',
                id:134
              },
              {
                name:'06-15',
                id:135
              },
              {
                name:'06-16',
                id:136
              },
              {
                name:'06-17',
                id:137
              },
              {
                name:'06-18',
                id:138
              },
            ]
          }
        ]
      },
      {
        name:'相约学习',
        id:2,
        children:[
          {
            name:'日期',
            id:21,
            children:[
              {
                name:'06-11',
                id:211
              },
              {
                name:'06-12',
                id:212
              },
              {
                name:'06-13',
                id:213
              },
              {
                name:'06-14',
                id:214
              },
              {
                name:'06-15',
                id:215
              },
              {
                name:'06-16',
                id:216
              },
              {
                name:'06-17',
                id:217
              },
              {
                name:'06-18',
                id:218
              },
            ]
          },
          {
            name:'科目',
            id:22,
            children:[
              {
                name:'请填写想要查找的科目名',
                id:221
              },
    
            ]
          }
        ]
      },
      {
        name:'约个球',
        id:3,
        children:[
          {
            name:'日期',
            id:31,
            children:[
              {
                name:'06-11',
                id:311
              },
              {
                name:'06-12',
                id:312
              },
              {
                name:'06-13',
                id:313
              },
              {
                name:'06-14',
                id:314
              },
              {
                name:'06-15',
                id:315
              },
              {
                name:'06-16',
                id:316
              },
              {
                name:'06-17',
                id:317
              },
              {
                name:'06-18',
                id:318
              },
            ]
          },
          {
            name:'项目',
            id:32,
            children:[
              {
                name:'请填写想要查找的运动',
                id:321
              },
   
            ]
          }
        ]
      },
      {
        name:'闲置交易',
        id:4,
        children:[
          {
            name:'物品类别',
            id:41,
            children:[
              {
                name:'钱包',
                id:411
              },
              {
                name:'钥匙',
                id:412
              },
              {
                name:'宠物',
                id:413
              },
              {
                name:'卡类/证照',
                id:414
              },
              {
                name:'数码产品',
                id:415
              },
              {
                name:'书籍/文件',
                id:416
              },
              {
                name:'衣服/鞋帽',
                id:417
              },
              {
                name:'首饰/挂饰',
                id:418
              },
              {
                name:'行李/包裹',
                id:419
              },
              {
                name:'手袋/挎包',
                id:4110
              },
              {
                name:'其它',
                id:4111
              },
            ]
          },
          {
            name:'物品名称',
            id:42,
            children:[
              {
                name:'请填写想要查找的物品名',
                id:421
              },
            ]
          },
          {
            name:'日期',
            id:43,
            children:[
              {
                name:'06-11',
                id:431
              },
              {
                name:'06-12',
                id:432
              },
              {
                name:'06-13',
                id:433
              },
              {
                name:'06-14',
                id:434
              },
              {
                name:'06-15',
                id:435
              },
              {
                name:'06-16',
                id:436
              },
              {
                name:'06-17',
                id:437
              },
              {
                name:'06-18',
                id:438
              },
            ]
          }
        ]
      },
      {
        name:'考研资讯',
        id:5,
        children:[
          {
            name:'日期',
            id:51,
            children:[
              {
                name:'06-11',
                id:511
              },
              {
                name:'06-12',
                id:512
              },
              {
                name:'06-13',
                id:513
              },
              {
                name:'06-14',
                id:514
              },
              {
                name:'06-15',
                id:515
              },
              {
                name:'06-16',
                id:516
              },
              {
                name:'06-17',
                id:517
              },
              {
                name:'06-18',
                id:518
              },
            ]
          },
          {
            name:'考研专业',
            id:52,
            children:[
              {
                name:'请填写想要了解的考研专业',
                id:521
              },
   
            ]
          }
        ]
      },
      {
        name:'论文推荐',
        id:6,
        children:[
          {
            name:'日期',
            id:61,
            children:[
              {
                name:'06-11',
                id:611
              },
              {
                name:'06-12',
                id:612
              },
              {
                name:'06-13',
                id:613
              },
              {
                name:'06-14',
                id:614
              },
              {
                name:'06-15',
                id:615
              },
              {
                name:'06-16',
                id:616
              },
              {
                name:'06-17',
                id:617
              },
              {
                name:'06-18',
                id:618
              },
            ]
          },
          {
            name:'论文简要标题',
            id:62,
            children:[
              {
                name:'请填写论文简要标题进行查找',
                id:621
              },
   
            ]
          }
        ]
      },
      {
        name:'菜鸟编程',
        id:7,
        children:[
          {
            name:'日期',
            id:71,
            children:[
              {
                name:'06-11',
                id:711
              },
              {
                name:'06-12',
                id:712
              },
              {
                name:'06-13',
                id:713
              },
              {
                name:'06-14',
                id:714
              },
              {
                name:'06-15',
                id:715
              },
              {
                name:'06-16',
                id:716
              },
              {
                name:'06-17',
                id:717
              },
              {
                name:'06-18',
                id:718
              },
            ]
          },
          {
            name:'相关技术',
            id:72,
            children:[
              {
                name:'请填写相关技术进行模糊查询',
                id:721
              },
   
            ]
          }
        ]
      },
      {
        name:'竞赛信息',
        id:8,
        children:[
          {
            name:'日期',
            id:81,
            children:[
              {
                name:'06-11',
                id:811
              },
              {
                name:'06-12',
                id:812
              },
              {
                name:'06-13',
                id:813
              },
              {
                name:'06-14',
                id:814
              },
              {
                name:'06-15',
                id:815
              },
              {
                name:'06-16',
                id:816
              },
              {
                name:'06-17',
                id:817
              },
              {
                name:'06-18',
                id:818
              },
            ]
          },
          {
            name:'比赛名称',
            id:82,
            children:[
              {
                name:'请填写比赛名称进行查询',
                id:821
              },
   
            ]
          }
        ]
      },
    ],

    imageUrl:"",
    allCategoryMessage: [],
    search: "",
    activeIndex: 1,
    isLastPage: false, //是否最后一页
    // 此页面 页面内容距最顶部的距离

    user_message: [],
    height: app.globalData.height * 2 + 20,
    input_subject: "",
    input_obj_name: "",
  },

  input_obj_name: function(e) {
    let value = e.detail.value;
    this.setData({
      input_obj_name: value
    })
  },

  input_subject: function(e) {
    let value = e.detail.value;
    this.setData({
      input_subject: value
    })
  },
  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {
    // 最后一页了，取消下拉功能
    if (this.data.isLastPage) {
      return
    }
    this.loadMessage(this.data.search, 1)
  },

  loadMessage(keyword, index) {
    let that = this;
    //失物招领+闲置交易
    if(that.data.picker_index[0]==0||that.data.picker_index[0]==3)
    {
      let list= that.data.picker_index[1]==0?{
        condition: 'object_class',
        value: that.data.picker_data[2].name
      }:that.data.picker_index[1]==1?{
        condition: 'object_name',
        value: that.data.input_obj_name     
      }:{
        condition: 'date_time_after',
        value: '2020-'+that.data.picker_data[2].name
      }
      wx.request({
        url: getApp().globalData.url + getApp().globalData.querycategoryurl[that.data.picker_index[0]],
        method: "POST",
        data: list,
        header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
        },
        success: function(e) {
          if (e.data.result.length == 0) {
            wx.showModal({
              title: '提示',
              content: '没有搜到噢，换个关键词吧',
            })
            return;
          }

          that.setData({
            user_message: that.data.user_message.concat(e.data.result.slice(that.data.skip,that.data.skip+5))
          })
          //下一次加载skip+1
        that.data.skip +=5
        if (e.data.result.slice(that.data.skip,that.data.skip+5).length == 0) {
          that.setData({
            isLastPage: true
          })
          return;
        } 
          
        }
      })
    }
    
    //相约学习+约个球+考研资讯+论文推荐+菜鸟编程+竞赛信息
    if(that.data.picker_index[0]!=0&&that.data.picker_index[0]!=3)
    {
      let list= that.data.picker_index[1]==0?{
        condition: 'date_time_after',
        value: '2020-'+that.data.picker_data[2].name
      }:{
        condition: 'object_name',
        value: that.data.input_subject   
      }
      wx.request({
        url: getApp().globalData.url + getApp().globalData.querycategoryurl[that.data.picker_index[0]],
        method: "POST",
        data: list,
        header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
        },
        success: function(e) {
          if (e.data.result.length == 0) {
            wx.showModal({
              title: '提示',
              content: '没有搜到噢，换个关键词吧',
            })
            return;
          }
        that.setData({
            user_message: that.data.user_message.concat(e.data.result.slice(that.data.skip,that.data.skip+5))
        })
          //下一次加载skip+1
        that.data.skip +=5
        if (e.data.result.slice(that.data.skip,that.data.skip+5).length == 0) {
          that.setData({
            isLastPage: true
          })
          return;
        } 
          
        }
      })
    }
  }, 
  
  //跳转到详情页
  to_message_detail: function(e) {
    wx.navigateTo({
      url: '/pages/message_detail/message_detail?messageId=' + e.currentTarget.id,
    })
  },

  showPicker: function () {
    this.setData({
      isShow: true
    })
  },

  sureCallBack (e) {
    let data = e.detail
    this.setData({
      isShow: false,
      picker_data: e.detail.choosedData,
      picker_index: e.detail.choosedIndexArr

    })
    // console.log(this.data.picker_data)
    // console.log(this.data.picker_data[2].name)
  },

  cancleCallBack () {
    this.setData({
      isShow: false,
    })
  },

  onLoad() {
    //获取日期
    var DATE = util.formatDate(new Date());
    this.setData({
    date: DATE,
    });
    /**
     * 分类信息
     */

    this.setData({
      allCategoryMessage: getApp().globalData.categoryMessage,
      imageUrl:getApp().globalData.imageUrl,
    })
    this.setData({
      height: app.globalData.height
    })
  }
})