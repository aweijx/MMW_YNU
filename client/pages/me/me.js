//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 0, //是否显示左上角图标   1表示显示    0表示不显示
      title: '我的', //导航栏 中间的标题
      height: 0
    },

    userId: "-1",
    message: {},
    userInfo: {},
    showDialog1: false,
    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
    isLoading: false
  },
  onLoad() {

    this.setData({
      height: app.globalData.height
    })
    var that = this
    wx.getStorage({
      key: 'userId',
      success: function(res) {
        that.setData({
          userId: res.data
        })
      },
      fail: function() {
        if (that.data.userId == -1) {
          that.setData({
            showDialog1: true
          })
        }
      }
    })
    wx.getStorage({
      key: 'userInfo',
      success: function(res) {
        that.setData({
          userInfo: res.data
        })
      },
      fail: function() {
        if (that.data.userId == -1) {
          that.setData({
            showDialog1: true
          })
        }
      }
    })
    that.setData({
      userInfo: getApp().globalData.userInfo,
      userId: getApp().globalData.userId
    })


  },
  checkAdmin() {
    let that = this
    wx.request({
      url: getApp().globalData.url + '/checkAdmin?id=' + new Number(that.data.userId),
      method: "post",
      success: function(res) {
        if (res.data[0].userIsAdmin != 2) {
          wx.showModal({
            title: '提示',
            content: '还未获得权限，请联系管理员',
          })
        }
        if (res.data[0].userIsAdmin == 2) {
          wx.showModal({
            title: '提示',
            content: '已获得管理员权限',
          })
        }
        wx.setStorage({
          key: 'userIsAdmin',
          data: res.data[0].userIsAdmin,
        })
        getApp().globalData.userIsAdmin = res.data[0].userIsAdmin
      }
    })
  },
  doLogin: function(e) {

    let that = this

    var list = {
      "nickName": e.detail.userInfo.nickName,
      "gender": e.detail.userInfo.gender,
      "city": e.detail.userInfo.city,
      "province": e.detail.userInfo.province,
      "country": e.detail.userInfo.country,
      "avatarUrl": e.detail.userInfo.avatarUrl
    }

    var listMessage = {
      "userAvatar": e.detail.userInfo.avatarUrl,
      "userNickname": e.detail.userInfo.nickName,
      "userGender": e.detail.userInfo.gender,
    }
    wx.login({
      success: function(res) {
        wx.showLoading({
          title: '登陆中~',
        })
        // console.log(that.data.openid)
        // 获取登录的临时凭证
        var code = res.code;
        // 调用后端，获取微信的session_key, secret
        //var d = that.globalData;
        var appId = 'wx12063e8256b4e57f';
        var secret = 'def506697c00c52eee357a377cf0f440';
        wx.request({
          url: 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code',
          data: {},
          header: {
            'content-type': 'json'
          },
          success: function (res) {
            var openid = res.data.openid //返回openid
            
            wx.setStorage({
              key: 'userId',
              data: openid,
            })
            that.setData({
              userId: openid
            })
            
            //console.log('userid为' + that.data.userId)
          }
        })
        wx.request({
          url: 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code',
          method: "GET",
          data: JSON.stringify(listMessage),
          dataType: JSON,
          success: function(result) {
            wx.hideLoading();
            if (result.statusCode != 200) {
              //console.log(result)
              wx.showModal({
                title: '提示',
                content: '出现问题啦，在试一下吧~',
              })
              return;
            }
            that.setData({
              message: JSON.parse(result.data),
              userInfo: list,
            })
            
            wx.setStorage({
              key: 'userInfo',
              data: list,
            })
            //登陆完成后全局变量记得要设置
            getApp().globalData.userInfo = list
            getApp().globalData.userId = that.data.userId
            //查看用户是否老用户
            //console.log('neworold:',that.data.userId)
            wx.request({
              url: getApp().globalData.url+'query_user_info',
              method: "POST",
              data:{
               "openid": that.data.userId,
              },
               header:{
                "content-type" : "application/x-www-form-urlencoded",
                "chartset" : "utf-8",
              },
              success:function(e){
                if (e.data.result.length>=1) {
                  wx.showModal({
                    title: '提示',
                    content: '欢迎回来，老朋友~',
                  })
                }
                if (e.data.result.length<=0) {
                  wx.showModal({
                    title: '提示',
                    content: '你好新朋友，快去探索吧~',
                  })
                  //添加用户信息
                  wx.request({
                    url: getApp().globalData.url+'add_user_info',
                    method: "POST",
                    data:{
                    "openid": that.data.userId,
                    "nick_name": that.data.userInfo.nickName,
                    "gender": that.data.userInfo.gender,
                  },
                    header:{
                      "content-type" : "application/x-www-form-urlencoded",
                      "chartset" : "utf-8",
                    },
                    success:function(e){

                    }
                  })
                }
              }
            })

            
            
            that.setData({
              showDialog1: false
            })
          }
        })
      }
    })
  },
  onReady() {
    let that = this
    setTimeout(function() {
      that.setData({
        isLoading: true
      })
    }, 500)
  },

  attention() {
    wx.showModal({
      title: '提示',
      content: '公众号名称  云大妙妙屋',
      confirmText: "复制",
      showCancel: false,
      success: function() {
        wx.setClipboardData({
          data: '云大妙妙屋',
        })
      }
    })
  },
  call() {
    wx.showModal({
      title: '提示',
      content: '微信联系/手机联系',
      confirmText: "手机联系",
      confirmColor: "#3cc",
      cancelColor: "#3cc",
      cancelText: "微信联系",
      success: function(e) {
        if (e.confirm) {
          wx.showModal({
            title: '提示',
            content: '是否联系(17608844790)',
            success: function(e) {
              if (e.confirm) {
                wx.makePhoneCall({
                  phoneNumber: '17608844790',
                })
              }
            }
          })
        } else {
          wx.showModal({
            title: '提示',
            content: '微信号：cwhhsmb',
            confirmText: "复制",
            success: function(e) {
              if (e.confirm) {
                wx.setClipboardData({
                  data: 'cwhhsmb',
                })
              }
            }
          })
        }
      }
    })
  },
  onShow() {
    let that = this
    this.setData({
      userId: getApp().globalData.userId
    })
    //console.log('userid:',that.data.userId)
    wx.getStorage({
      key: 'userId',
      success: function(res) {
        that.setData({
          userId: res.data
        })
      },
    })
    //用户登陆频繁，需要等五分钟重新登陆
    if(that.data.userId==undefined)
    {
      wx.showModal({
        title: '提示',
        content: '登陆太频繁了哟，等五分钟再试一下吧~',
      })
    }
    
  }
})