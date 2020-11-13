//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '我的收藏', //导航栏 中间的标题
      height: 0
    },
    skip:0,//第几次加载
    imageUrl:"",
    allCategoryMessage: [],
    userId: -1,
    activeIndex: 0,
    floorstatus: "none",
    user_message: [],

    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
    isLoading: false
  },
  onReady() {
    let that = this
    setTimeout(function() {
      that.setData({
        isLoading: true
      })
    }, 500)
  },
  onLoad() {
    let that = this
    this.setData({
      imageUrl:getApp().globalData.imageUrl,
      allCategoryMessage: getApp().globalData.categoryMessage
    })
    this.setData({
      height: app.globalData.height
    })
    this.setData({
      userId: getApp().globalData.userId
    })
    this.loadMessage(1)


  },
  loadMessage(index) {
    wx.showLoading({
      title: '加载中~',
    })
    var that = this;
    var app = getApp()
    wx.request({
      url: getApp().globalData.url+'/query_attention_by_user',
      data:{
        'openid':getApp().globalData.userId,
        // page_index:0
      },
      method: "POST",
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: (res) => {
        if (res.statusCode != 200) {
          wx.showModal({
            title: '提示',
            content: '出错啦，请稍后再试~',
          })
          return;
        }
        that.setData({          
          user_message: that.data.user_message.concat(res.data.result.slice(that.data.skip,that.data.skip+5))
        })
        //下一次加载skip+1
        that.data.skip +=5
        if (res.data.result.slice(that.data.skip,that.data.skip+5).length == 0) {
          that.setData({
            isLastPage: true
          })
          return;
        } 
        
      },
      complete: function(res) {
        wx.hideLoading();
      },
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
    this.loadMessage(++this.data.activeIndex)
  },
  //一键返回顶部
  onPageScroll: function(e) { //判断滚轮位置
    if (e.scrollTop > 200) {
      this.setData({
        floorstatus: "block"
      });
    } else {
      this.setData({
        floorstatus: "none"
      });
    }
  },

  goTop: function(e) { // 一键回到顶部
    if (wx.pageScrollTo) {
      wx.pageScrollTo({
        scrollTop: 0
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
      })
    }
  }, //跳转到详情页
  to_message_detail: function(e) {
    wx.navigateTo({
      url: '/pages/message_detail/message_detail?messageId=' + e.currentTarget.id,
    })
  },
})