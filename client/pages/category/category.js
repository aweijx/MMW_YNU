//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '分类', //导航栏 中间的标题
      height: 0
    },
    imageUrl:"",
    //allCategoryMessage: [],
    skip:0,//第几次加载
    search: "",
    floorstatus: "none",
    user_message: [],
    commentsize: 0,
    activeIndex: 1,
    isLastPage: false, //是否最后一页
    categoryId: -1,
    categoryName: "", //用于类别flag显示
    querycategoryurl: [],
    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
    isLoading: false
  },
  // activity_clear() {
  //   this.setData({
  //     search: ""
  //   })
  // },
  // endsearchList: function(e) {
  //   let that = this;
  //   if (this.data.search.length < 2) {
  //     wx.showModal({
  //       title: '提示',
  //       content: '至少输入两个字噢~',
  //       showCancel: false
  //     })
  //     return;
  //   }
  //   wx.request({
  //     url: getApp().globalData.url + '/search/' + that.data.categoryId + '/' + that.data.search,
  //     method: "post",
  //     success: function(e) {
  //       if (e.data.length == 0) {
  //         wx.showModal({
  //           title: '提示',
  //           content: '没有搜到噢，换个关键词吧',
  //         })
  //         return;
  //       }

  //       that.setData({
  //         user_message: e.data,
  //         isLastPage: true
  //       })
  //     }
  //   })
  // },
  // searchList: function(e) {
  //   let value = e.detail.detail.value;
  //   this.setData({
  //     search: value
  //   })
  // },
  onLoad(options) {


    this.setData({
      //allCategoryMessage: getApp().globalData.categoryMessage,
      imageUrl:getApp().globalData.imageUrl,
      querycategoryurl: getApp().globalData.querycategoryurl,
    })
    this.setData({
      height: app.globalData.height,
      categoryId: options.categoryId,
      categoryName: options.categoryName
    })
    this.setData({
      nvabarData: {
        showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
        title: options.categoryName, //导航栏 中间的标题
        height: 0
      }
    })
    this.loadMessage(options.categoryId, 1)

  },
  loadMessage(categoryId, page) {
    let that = this;
    var app = getApp()
    wx.request({
      //url: getApp().globalData.url + '/getMessage/getAllMessageDetail/' + categoryId + '/' + page,
      url: getApp().globalData.url+that.data.querycategoryurl[categoryId],
      method: "POST",
      data:{
        "condition": 'date_time_after',
        "value": '2020-06-04',
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: (res) => {
        console.log(res)
          // if (page == 2) {
          //   that.setData({
          //     isLastPage: true
          //   })
          //   return;
          // }    
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

        setTimeout(function() {
          that.setData({
            isLoading: true
          })
        }, 300)

        wx.stopPullDownRefresh();//停止刷新操作
      },
    })

    /*
    获得留言数目
    */
   
  //  wx.request({
  //    url: 'http://124.70.144.48:8080/',
  //  })
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    // wx.showToast({
    //   title: '正在刷新数据...',
    //   icon: 'loading',
    //   duration: 2000
    // });
    this.setData({user_message:[],isLastPage: false,activeIndex: 1,skip: 0});//先清空数据
    this.loadMessage(this.data.categoryId,1);//再重新加载数据
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
  },
  //跳转到详情页
  to_message_detail: function(e) {
    wx.navigateTo({
      url: '/pages/message_detail/message_detail?messageId=' + e.currentTarget.id,
    })
  },
  onReachBottom: function(e) {
    // 最后一页了，取消下拉功能
    if (this.data.isLastPage) {
      return
    }
    this.loadMessage(this.data.categoryId, 1)
  },
})