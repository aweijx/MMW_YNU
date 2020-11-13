//index.js
//获取应用实例
const app = getApp()
//var bmap = require('../../utils/bmap-wx.min.js');
Page({
  data: {
    imageUrl:"",
    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
    currentIndex: 0,
    a1src:'../../images/other/shiwuzhaoling.png',
    a2src: '../../images/other/xuexi.png',
    a3src: '../../images/other/lanqiu.png',
    a4src: '../../images/other/xiaoyuanzulin.png',
    a5src:'../../images/other/kaoyan.png',
    a6src: '../../images/other/lunwen.png',
    a7src: '../../images/other/biancheng.png',
    a8src: '../../images/other/jingsai.png',
    //allCategoryMessage: [],
    //weatherData: null,
    floorstatus: "none",
    categoryname: ["失物招领","相约学习","约个球","闲置交易","考研资讯","论文推荐","菜鸟编程","竞赛信息"],
    notice: 
      [
        "欢迎来到云大妙妙屋，快去发布消息吧！",
        "如果有问题，请在我的界面联系我们哟！"
      ],
    //lost_new: {},
    //takeout: [],
    ad_bottom: ["../../images/other/ad_bottom.jpg"],
    user_message: [],
    activeIndex: 0,
    isLastPage: false, //是否最后一页
    isUpdate: -1,
    isLoading: false //页面是否渲染完毕
  },
  onReady() {
    let that = this
    setTimeout(function() {
      that.setData({
        isLoading: true
      })
    }, 1000)

  },

  // /**
  //  * 联系我
  //  */
  // me_call() {
  //   wx.showModal({
  //     title: '提示',
  //     content: '如有需要请联系我',
  //     confirmText: "联系我",
  //     success: function(e) {
  //       if (e.confirm) {
  //         wx.makePhoneCall({
  //           phoneNumber: '',
  //         })
  //       }
  //     }
  //   })
  // },
  // //查看失物招领详情
  // lookLostMessage(e) {
  //   wx.showModal({
  //     title: '失物招领',
  //     content: e.target.id,
  //     showCancel: false,
  //     confirmText: '已查阅'
  //   })
  // },
  // //查看最新的失物招领
  // new_lost_look(e) {
  //   wx.navigateTo({
  //     url: "/pages/message_detail/message_detail?messageId=" + e.currentTarget.id
  //   })
  // },
  //预览图片
  previewImg: function (e) {
    var currentUrl = e.currentTarget.dataset.currenturl
    var previewUrls = e.currentTarget.dataset.previewurl
    wx.previewImage({
      current: currentUrl, //必须是http图片，本地图片无效
      urls: previewUrls, //必须是http图片，本地图片无效
    })
  },
  //查看公告
  checkNotice(e) {
    var index = e.currentTarget.dataset.index
    wx.showModal({
      title: '公告',
      content: this.data.notice[index],
      showCancel: false,
      confirmText: '已查阅'
    })
  },
  //授权天气
  // getWeatherData() {
  //   let that = this;
  //   wx.openSetting({
  //     success: function(res) {
  //       if (res.authSetting && res.authSetting["scope.userLocation"]) {
  //         //允许授权,则自动获取定位，并关闭二确弹窗，否则返回首页不处理
  //         wx.showToast({
  //           title: '您已授权获取位置信息',
  //           icon: 'none'
  //         })
  //         that.getWeather();
  //       } else {
  //         wx.showToast({
  //           title: '需要授权才可以查看天气噢~',
  //           icon: 'none'
  //         })
  //       }
  //     }
  //   })
  // },
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
  //跳转到搜索页
  search: function() {
    wx.navigateTo({
      url: '/pages/search/search',
    })
  },
  //跳转到详情页
  to_message_detail: function(e) {
    wx.navigateTo({
      url: '/pages/message_detail/message_detail?messageId=' + e.currentTarget.id,
    })
  },

  // getWeather() {
  //   var that = this;
  //   // 新建百度地图对象 
  //   var BMap = new bmap.BMapWX({
  //     ak: '1yb9NASdSjEYoxhTj59uD1qdyCHgKE6U'
  //   });
  //   var fail = function(data) {

  //   };
  //   var success = function(data) {
  //     var weatherData = data.currentWeather[0];
  //     that.setData({
  //       weatherData: weatherData
  //     });

  //   }
    // 发起weather请求 
  //   BMap.weather({
  //     fail: fail,
  //     success: success
  //   });
  // },

 
  onLoad: function(options) {
  /*
    设置轮播图，可能影响加载速度
  */
    let that = this
    var picList = []
    picList.push(getApp().globalData.imageUrl+"2.jpg")
    picList.push(getApp().globalData.imageUrl+"1.png")
    picList.push(getApp().globalData.imageUrl+"3.png")
    picList.push(getApp().globalData.imageUrl+"4.png")
    that.setData({
      picList: picList,
    })
    //this.getWeather();
    /**
     * 图片路径
     */
    this.setData({
      //takeout: getApp().globalData.shopMessage,
      imageUrl:getApp().globalData.imageUrl,
    })

    /**
     * 公告信息
     */

    /**
     *第一页最新信息
     */
    this.setData({
      user_message: getApp().globalData.messageDetail
    })

  },
  handleImgChange: function(e) {
    this.setData({
      currentIndex: e.detail.current
    })
  },

  /**
   * 下拉
   */
  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    this.setData({user_message:[],isLastPage: false,activeIndex: 0});//先清空数据
    this.loadMessage(0);//再重新加载数据
  },
  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {
    // 最后一页了，取消下拉功能
    if (this.data.isLastPage) {
      this.loadMessage(++this.data.activeIndex)
      return
    }
    this.loadMessage(++this.data.activeIndex)
  },

  loadMessage(index) {
    wx.showLoading({
      title: '加载中~',
    })
    //console.log(index)
    var that = this;
    var app = getApp()
    wx.request({
      //url: getApp().globalData.url + '/getMessage/getAllMessageDetail/' + index,
      url: getApp().globalData.url+'query_latest_info',
      method: "POST",
      data:{
        "page_index": index,
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: (res) => {

        that.setData({
          user_message: that.data.user_message.concat(res.data.result)
        })

        if (res.data.result.length < 20) {
          that.setData({
            isLastPage: true
          })
          return;
        }
        
      },
      complete: function(res) {
        wx.hideLoading();
        wx.stopPullDownRefresh();//停止刷新操作
      },
    })

  },
  onShow() {
    let that = this
    /*
    提示新消息
    */
    wx.request({
      //url: getApp().globalData.url + '/getMessage/getLastNewMessage/' + getApp().globalData.userId,
      url: getApp().globalData.url+'/query_message_to_user',
      data:{
        'openid':getApp().globalData.userId,
        // page_index:0
      },
      method: "POST",
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      complete: function(e) {

        if (e.statusCode != 200||e.data.result.length==0) {
          return
        }

        wx.getStorage({
          key: 'lastNewMessage',
          success: function(res) {
            //console.log('msg',res.data)
            if (res.data != e.data.result[0].MSG_ID) {
              wx.playBackgroundAudio({
                dataUrl: 'http://downsc.chinaz.net/Files/DownLoad/sound1/201609/7824.wav',
                title: '提示',
              })
              wx.showModal({
                title: '新消息',
                content: '内容：' + e.data.result[0].MSG,
                confirmText: "去查看",
                cancelText: "稍后去看",
                success: function(e) {
                  if (e.confirm) {
                    wx.navigateTo({
                      url: '/pages/me_xiaoxi/me_xiaoxi',
                    })
                  }
                }
              })
            }
          },
        })

        wx.setStorage({
          key: 'lastNewMessage',
          data: e.data.result[0].MSG_ID,
        })
      }

    })
    /**
     * 判断是否更新
     */
    if (getApp().globalData.isUpdate == 1) {
        this.setData({
          user_message: [],
          activeIndex: 0,
          isLastPage: false, //是否最后一页
        }),
        this.loadMessage(0),
      getApp().globalData.isUpdate = -1
    }

  },
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {
    return {
      title: "云大妙妙屋，你的校园专属助手",
      imageUrl: "../../images/other/logo.png"
    }

  }
  
})