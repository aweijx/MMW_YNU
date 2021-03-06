//index.js
//获取应用实例
const app = getApp()
var judge = require('../../utils/judge.js');

Page({
  
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '我的发布', //导航栏 中间的标题
      height: 0
    },
    updateurl:'',
    delurl:'del_found_info',
    end:0,
    status:'',
    array:['已找到','没找到','已售','没卖'],
    URL:app.globalData.imageUrl,
    imageUrl:"",
    allCategoryMessage: [],
    showDialog1: false,
    //showDialog2: false,
    currentIndex: -1,
    userId: -1,
    openid:'',
    categoryname:'',
    user_message: [],
    floorstatus: "none",
    activeIndex: 1,
    isLastPage: false, //是否最后一页
    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
    updatestatus: "",
    isLoading: false,
    category_index:null
  },

  temUpdateMessage(e) {

    this.setData({
      category_index: e.detail.value,
      
    })
    // this.data.updateMessage=this.data.array[e.detail.value]


  },

  updateMessage(status) {
    let that = this
     this.setData({
      // queryurl: getApp().globalData.querycategoryurl[urlindex],
      updateurl: that.data.status=="没找到"||that.data.status=='已找到'?'update_found_status'
      :'update_second_hand_status',
      updatestatus: judge.judgestatus(that.data.status),
    })
      // if (this.data.updateMessage == this.data.status) {
      //   wx.showModal({
      //     title: '提示',
      //     content: '好像没有什么变化噢~',
      //   })
      //   return;
      // }
      if (this.data.userId == -1) {
        wx.showModal({
          title: '提示',
          content: '好像出问题啦，退出去重新试试吧~',
        })
        return;
      }
      wx.showLoading({
        title: '更新中~',
      })
      wx.request({
        //url: getApp().globalData.url + '/updateMessageById/' + that.data.userId + '/' + that.data.user_message[that.data.currentIndex].messageId,
        url: getApp().globalData.url + that.data.updateurl,
              method: "POST",
              // data:{
              //   "openid": this.data.openid,
              //   "object_id": this.data.categoryname,
              // },
              data:{
                "openid": that.data.userId,
                "object_id": that.data.categoryname,
                "object_status":that.data.updatestatus
              },
              header:{
                "content-type" : "application/x-www-form-urlencoded",
                "chartset" : "utf-8",
              },
        success: function(e) {
          if (e.statusCode != 200) {
            wx.showModal({
              title: '提示',
              content: '好像出问题啦，退出去重新试试吧~',
            })
            return;
          }
          wx.hideLoading()
          if (e.statusCode == 200) {   //改动e.data.code->e.statusCode
            wx.showModal({
              title: '提示~',
              content: '更新成功啦~',
            })
           
            that.setData({
              user_message: [],
              showDialog1: false,
              //showDialog2: false,
            })
            that.onLoad();
          }
        }
      })
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

  toggleDialog2() {
    let that = this;
    wx.showModal({
      title: '提示',
      content:  '请问是否更新物品状态为'+judge.judgestatus(that.data.status),
      showCancel: true,
      success:function(res){
        if(res.confirm){
          wx.showLoading({
            title: '更新状态信息中~',
          })
          that.updateMessage(0)
        }
      }
    })
  },

  toggleDialog1(e) {

    this.setData({
      showDialog1: !this.data.showDialog1,
      categoryname:e.currentTarget.dataset.total,
      openid:e.currentTarget.dataset.open,
      status:e.currentTarget.dataset.status
    });

    // this.setCurrentIndex(e.currentTarget.dataset.tatal)
  },
  //设置当前索引值
  setCurrentIndex() {

    // this.setData({
    //   currentIndex: id
    // })
    // this.setData({
    //   updateMessage: this.data.user_message[id].messageDetail
    // })
  },
  //查看详情
  to_look_detail(e) {
    let that = this
    wx.navigateTo({
      url: '/pages/message_detail/message_detail?messageId=' + that.data.categoryname,
    })
  },
  //删除信息
  delete_message(id) {
    let that = this
    var categoryname1 = this.data.categoryname.slice(0,5);//取object_id前五个元素看是哪个类型

     this.setData({
      // queryurl: getApp().globalData.querycategoryurl[urlindex],
      delurl: getApp().globalData.delmessageurl[judge.judgeurl(categoryname1)]
    })
    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '出现错误，请稍后再试~',
      })
      return;
    }

    wx.showModal({
      title: '提示',
      content: '是否删除?',
      confirmColor: "#f00",
      success: function(e) {

        if (e.confirm) {
          wx.showLoading({
            title: '稍等噢~',
          })
          that.setData({
            showDialog1: false
          });
          wx.request({
            url: getApp().globalData.url + that.data.delurl,
            method: "POST",
            // data:{
            //   "openid": this.data.openid,
            //   "object_id": this.data.categoryname,
            // },
            data:{
              "openid": that.data.userId,
              "object_id": that.data.categoryname,
            },
            header:{
              "content-type" : "application/x-www-form-urlencoded",
              "chartset" : "utf-8",
            },
            success: function(e) {
              wx.hideLoading()
              if (e.statusCode != 200) {
                wx.showModal({
                  title: '提示',
                  content: '服务器出现错误，请稍后再试',
                  showCancel: false
                })
                return;
              }
                wx.showModal({
                  title: '提示',
                  content: '删除成功',
                  showCancel: false,
                  success: function() {
                    wx.showLoading({
                      title: '更新主页信息中~',
                    })
                    that.onLoad();
                    wx.hideLoading();
                  },

                })
            }
          })
        }
      }
    })
  },
  updateAllMessage() {
    let that = this;
    /**
     * 获取最新
     */
    wx.request({
      url:getApp().globalData.url+'/query_latest_by_user',
      data:{
        'openid':getApp().globalData.userId,
        // page_index:0
      },
      method: "POST",
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: function(e) {
        that.setData({
          user_message:res.data.result,
          // end:1
        })
      }
    })

    getApp().globalData.isUpdate = 1;
  },
  onLoad(e) {

    let that = this
    this.setData({
      allCategoryMessage: getApp().globalData.categoryMessage,
      imageUrl:getApp().globalData.imageUrl,
    })
    this.setData({
      height: app.globalData.height
    })
    
    this.setData({
      userId: getApp().globalData.userId
    })

    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '出现错误，请稍后再试~',
      })
      return;
    }
    this.loadMessage(1)
  },
  loadMessage(index) {
    wx.showLoading({
      title: '加载中~',
    })
    var that = this;
    var app = getApp()
    wx.request({
      url: getApp().globalData.url+'/query_latest_by_user',
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
        if (this.data.end==1) {
          that.setData({
            isLastPage: true
          })
          return;
        }
        that.setData({
          user_message: res.data.result,
          // end:1
        })
        
      },
      complete: function(res) {
        wx.hideLoading();
      },
    })
  },
  onReady() {
    let that = this
    setTimeout(function () {
      that.setData({
        isLoading: true
      })
    }, 500)
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

  onShareAppMessage() {
    let that = this
    return {
      title: "来观看下~",
      path: '/pages/message_detail/message_detail?messageId=' + that.data.categoryname
    }
  }
})