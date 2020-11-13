//app.js
App({
//
  globalData: {
    share: false, // 分享默认为false
    height: 0,
    url: "http://116.63.183.139:80/",
    imageUrl: "http://116.63.183.139/",//这是你的oss地址,用来展示图片,后面加斜杠
    userId: "-1",
    userInfo: {},
    userIsAdmin: -1,
    shopMessage: [],
    swiperImages: ['http://116.63.183.139/2.jpg','http://116.63.183.139/1.png','http://116.63.183.139/3.png','http://116.63.183.139/4.png' ],
    categoryMessage: [],
    categoryid: [0,1,2,3,4,5,6,7],
    categoryname: ["失物招领","相约学习","约个球","闲置交易","考研资讯","论文推荐","菜鸟编程","竞赛信息"],
    categoryurl: ['add_found_info','add_study_info','add_play_info','add_second_hand_info','add_postgraduate_info','add_paper_info','add_code_info','add_contest_info'],
    querycategoryurl: ['query_found_info','query_study_info','query_play_info','query_second_hand_info','query_postgraduate_info','query_paper_info','query_code_info','query_contest_info'],
    delmessageurl: ['del_found_info','del_study_info','del_play_info','del_second_hand_info','del_postgraduate_info','del_paper_info','del_code_info','del_contest_info'],
    updata_status: ['update_found_status','update_second_hand_status'],
    shareurl:['update_found_forward','update_study_forward','update_play_forward','update_second_hand_forward','update_postgraduate_forward','update_papers_forward','update_code_forward','update_contest_forward'],
    alluserInfo: [],
    // noticeMessage: [],
    messageDetail: [],
    isUpdate: -1,
  },
  onLaunch: function (options) {

    wx.showLoading({
      title: '努力加载中~',
    })
    let that = this;
    // 判断是否由分享进入小程序
    if (options.scene == 1007 || options.scene == 1008) {
      this.globalData.share = true
    } else {
      this.globalData.share = false
    }
    //获取设备顶部窗口的高度（不同设备窗口高度不一样，根据这个来设置自定义导航栏的高度）
    //这个最初我是在组件中获取，但是出现了一个问题，当第一次进入小程序时导航栏会把
    //页面内容盖住一部分,当打开调试重新进入时就没有问题，这个问题弄得我是莫名其妙
    //虽然最后解决了，但是花费了不少时间
    wx.getSystemInfo({
      success: (res) => {
        this.globalData.height = res.statusBarHeight
      }
    })

    wx.getStorage({
      key: 'userId',
      success: function (res) {
        getApp().globalData.userId = res.data
      },
    })

    wx.getStorage({
      key: 'userInfo',
      success: function (res) {
        getApp().globalData.userInfo = res.data
      },
    })
    wx.getStorage({
      key: 'userIsAdmin',
      success: function (res) {
        getApp().globalData.userIsAdmin = res.data
      },
    })
    /**
     * 获取所有用户信息
     */
    wx.getStorage({
      key: 'alluserInfo',
      success: function(res){
        that.globalData.alluserInfo = res.data
        if(that.globalData.alluserInfo.length != res.data.length){
          wx.request({
            url: that.globalData.url+'/query_user_info',
            method : "POST",
            data:{
              "condition" : 'openid',
              "value" : '',
            },
            header:{
              "content-type" : "application/x-www-form-urlencoded",
              "chartset" : "utf-8",
            },
            success: function(res){
              that.globalData.alluserInfo = res.data.result
              wx.getStorage({
                key: 'alluserInfo',
                data: res.data.result,
              })
            }
          })
        }
      }
    })


    /**
     * 获取公告
     */
    // wx.request({
    //   url: that.globalData.url + '/getMessage/getAllNoticeMessage',
    //   method: "post",
    //   success: function (e) {
    //     that.globalData.noticeMessage = e.data
    //   }
    // })

    /**
     * 获取最新第一页消息
     */

      wx.request({
        url: that.globalData.url + 'query_latest_info',
        method: "POST",
        data:{
          "page_index": 0,
        },
        header:{
          "content-type" : "application/x-www-form-urlencoded",
          "chartset" : "utf-8",
        },
        success: function (e) {         
            that.globalData.messageDetail= that.globalData.messageDetail.concat(e.data.result)     
        }
      })
    

    // /*
    // 对最新发布按时间排序
    // */

    // var arr = that.globalData.messageDetail;
    // function compare(property){
    //   return function(a,b){
    //     var value1 = a[property];
    //     var value2 = b[property];
    //     return value1-value2;
    //   }
    // }

    //   that.globalData.messageDetail= arr.sort(compare('DATE_TIME'))

    /**
     * 获取最新失物招领
     */
    // wx.request({
    //   url: that.globalData.url + '/getMessage/getLostMessage',
    //   method: "post",
    //   success: function (e) {
    //     that.globalData.lost_new = e.data
    //   }
    // })
    wx.hideLoading()
  },


})
