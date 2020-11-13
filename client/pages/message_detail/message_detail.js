//index.js
//获取应用实例
const app = getApp()
var getcomment = require('../../utils/getcomment.js');
var judge = require('../../utils/judge.js');

Page({
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '详情', //导航栏 中间的标题
      height: 0,
    },
    imageUrl:"",
    showDialog1: false,
    showDialog2: false,
    showDialog3: false,
    showDialog4: false,
    floorstatus: "none",
    userIsAdmin: -1, //是否为管理员
    queryurl: "",
    delurl: "",
    userId: -1,
    userInfo: {},
    comment_input: "",
    comment_reply: "",
    liuyanName: "",
    pinglunName: "",
    //commentId: -1,
    receiveUserId: -1,
    commentUserId: -1,
    messageDetail: {},
    user_reply: [],
    user_comment: [],
    isCollection: false,
    attentionsize: 0, 
    group_id: 0,
    comment_group_id: 0,
    //key_comment: [0],
    //key_reply[1,],
    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
    isLoading: false //页面是否渲染完毕
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
  admin() {
    let that = this;
    if (that.data.userIsAdmin != 2) {
      return
    }
    wx.showModal({
      title: '信息',
      content: "手机号:" + that.data.messageDetail.userPhone + ",用户Id:" + that.data.messageDetail.userId + ",用户名:" + that.data.messageDetail.mangoUser.userNickname + ",文章id:" + that.data.messageDetail.messageId,
      cancelText: "复制号码",
      confirmText: "系统回复",
      success: function(e) {
        if (e.confirm) {
          that.setData({
            showDialog4: true
          })
        } else {
          wx.setClipboardData({
            data: that.data.messageDetail.userPhone + "",
          })
        }
      }
    })

  },

  toggleDialog4() {
    this.setData({
      showDialog4: false
    })
  },
  /**
   * 管理员回复消息
   */
  // admin_reply() {
  //   let that = this;
  //   if (that.data.userId == -1) {
  //     wx.showModal({
  //       title: '提示',
  //       content: '好像没有登录噢~',
  //     })
  //     return
  //   }
  //   wx.showLoading({
  //     title: '回复中~',
  //   })
  //   that.setData({

  //     showDialog4: false
  //   })
  //   wx.request({
  //     url: getApp().globalData.url + '/addNewMessageByAdmin/' + that.data.userId + '/' + that.data.messageDetail.messageId + "/" + that.data.messageDetail.userId,
  //     data: that.data.comment_reply,
  //     method: "post",
  //     success: function(e) {
  //       that.setData({
  //         comment_reply: "",
  //       })
  //       if (e.statusCode != 200) {
  //         wx.showModal({
  //           title: '提示',
  //           content: '系统错误',
  //         })
  //         return
  //       }

  //       if (e.data != 200) {
  //         wx.showModal({
  //           title: '提示',
  //           content: '系统错误',
  //         })
  //         return
  //       } else {
  //         wx.showModal({
  //           title: '提示',
  //           content: '回复成功',
  //         })

  //       }


  //     },
  //     complete: function() {
  //       wx.hideLoading()
  //     }
  //   })

  // },

  delete_comment(e) {
    let that = this;
    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '好像没有登录噢~',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: '/pages/me/me',
            })
            return;
          }
        }
      })
    }

    wx.showModal({
      title: '提示',
      content: '是否删除当前回复~',
      success: function(res) {
        if (res.confirm) {
          wx.request({
            //url: getApp().globalData.url + '/deleteCommentByCommentId/' + that.data.userId + '/' + e.target.id,
            url: getApp().globalData.url+'del_by_message_id',
            method: "POST",
            data: {
              //"openid": that.data.userId,
              "object_id": that.data.messageDetail.OBJECT_ID,
              "message_id": e.target.id,
            },
            header:{
              "content-type" : "application/x-www-form-urlencoded",
              "chartset" : "utf-8",
            },
            success: function(result) {

              if (result.statusCode != 200) {
                wx.showModal({
                  title: '提示',
                  content: '服务器出现问题，请稍后再试',
                })
                return;
              }

              if (result.statusCode == 200) {
                wx.showModal({
                  title: '提示',
                  content: '删除成功~',
                  success: function() {
                    wx.request({
                      //url: getApp().globalData.url + '/getMessageDetailById/' + that.data.messageDetail.messageId,
                      url: getApp().globalData.url+'query_message_by_obj',
                      method: "POST",
                      data:{
                         "object_id": that.data.messageDetail.OBJECT_ID,
                     },
                      header:{
                       "content-type" : "application/x-www-form-urlencoded",
                       "chartset" : "utf-8",
                      },
                      success: function(e) {
                        if(e.data.result==null||e.data.result.length==0||(e.data.result.length==1&&e.data.result[0].length==0))
                        {
                          that.setData({
                            user_comment: [],
                            user_reply: [],
                          })
                          return;
                        }
                        //console.log(comment)
                        that.setData({
                          user_comment: getcomment.comment(e.data.result),
                          user_reply: getcomment.reply(e.data.result),
                        })
                      }
                    })
                  }
                })
              }

            }
          })
        }
      }
    })

  },

  delete_comment_reply(e) {
    let that = this;
    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '好像没有登录噢~',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: '/pages/me/me',
            })
            return;
          }
        }
      })
    }
    wx.showModal({
      title: '提示',
      content: '是否删除当前内容~',
      success: function(res) {
        if (res.confirm) {
          wx.request({
            //url: getApp().globalData.url + '/deleteCommentByCommentId/' + that.data.userId + '/' + e.target.id,
            url: getApp().globalData.url+'del_by_message_id',
            method: "POST",
            data: {
              //"openid": that.data.userId,
              "object_id": that.data.messageDetail.OBJECT_ID,
              "message_id": e.target.id,
            },
            header:{
              "content-type" : "application/x-www-form-urlencoded",
              "chartset" : "utf-8",
            },
            success: function(result) {

              if (result.statusCode != 200) {
                wx.showModal({
                  title: '提示',
                  content: '服务器出现问题，请稍后再试',
                })
                return;
              }

              if (result.statusCode == 200) {
                wx.showModal({
                  title: '提示',
                  content: '删除成功~',
                  success: function() {
                    wx.request({
                      //url: getApp().globalData.url + '/getMessageDetailById/' + that.data.messageDetail.messageId,
                      url: getApp().globalData.url+'query_message_by_obj',
                      method: "POST",
                      data:{
                         "object_id": that.data.messageDetail.OBJECT_ID,
                     },
                      header:{
                       "content-type" : "application/x-www-form-urlencoded",
                       "chartset" : "utf-8",
                      },
                      success: function(e) {
                        if(e.data.result==null||e.data.result.length==0||(e.data.result.length==1&&e.data.result[0].length==0))
                        {
                          that.setData({
                            user_comment: [],
                            user_reply: [],
                          })
                          return;
                        }
                      
                        that.setData({
                          user_comment: getcomment.comment(e.data.result),
                          user_reply: getcomment.reply(e.data.result),
                        })
                      }
                    })
                  }
                })
              }

            }
          })
        }
      }
    })


  },
  test() {
    let that = this;
    let list = {
      group_id: that.data.group_id,
      openid: that.data.userId,
      object_id: that.data.messageId,
      msg: that.data.comment_reply,
      nick_name: that.data.userInfo.nickName,
      target_id: that.data.commentUserId,
      gender: that.data.userInfo.gender,
      // replayUserName: this.data.userInfo.nickName,
      // replyDetail: this.data.comment_reply,
      // receiveUserName: this.data.pinglunName,
      // receiveUserId: this.data.commentUserId,
      // commentUserId: this.data.commentUserId,
      // commentId: this.data.commentId,
    }

    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '好像没有登录噢~',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: '/pages/me/me',
            })
            return;
          }
        }
      })
    }

    if (that.data.comment_reply.length < 3) {
      wx.showModal({
        title: '提示',
        content: '至少输入三个字噢~',
      })
      return
    }

    that.setData({
      showDialog3: false,
    })
    wx.showLoading({
      title: '稍等噢~',
    })
    wx.request({
      //url: getApp().globalData.url + '/addCommentReply/' + that.data.messageDetail.messageId,
      url: getApp().globalData.url+'add_message',
      method: "POST",
      data: list,
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: function(e) {
        wx.hideLoading()
        if (e.statusCode != 200) {
          wx.showModal({
            title: '提示',
            content: '服务器出现问题，请稍后再试',
          })
          return;
        }

        if (e.statusCode == 200) {
          wx.showModal({
            title: '提示',
            content: '回复成功~',
            success: function() {
              wx.request({
                //url: getApp().globalData.url + '/getMessageDetailById/' + that.data.messageDetail.messageId,
                url: getApp().globalData.url+'query_message_by_obj',
                method: "POST",
                data:{
                  "object_id": that.data.messageId,
                },
                header:{
                  "content-type" : "application/x-www-form-urlencoded",
                  "chartset" : "utf-8",
                },
                success: function(e) {
                  
                  that.setData({
                    comment_reply: "",
                    user_comment: getcomment.comment(e.data.result),
                    user_reply: getcomment.reply(e.data.result),
                  })
                  //console.log(e.data.result)
                }
              })
            }
          })
        }

        if (e.data.code == 301) {
          wx.showModal({
            title: '提示',
            content: '你已被管理员禁止发布，详情请联系管理员',
            showCancel: false
          })
        }

      }
    })

  },
  /**
   * 回复，返回服务器
   */
  comment_reply_btn() {
    let that = this;
    let list = {
      group_id: that.data.group_id,
      openid: that.data.userId,
      object_id: that.data.messageId,
      msg: that.data.comment_reply,
      nick_name: that.data.userInfo.nickName,
      target_id: that.data.commentUserId,
      gender: that.data.userInfo.gender,
      // replayUserId: this.data.userId,
      // replayUserName: this.data.userInfo.nickName,
      // replyDetail: this.data.comment_reply,
      // receiveUserName: this.data.liuyanName,
      // receiveUserId: this.data.commentUserId,
      // commentUserId: this.data.commentUserId,
      // commentId: this.data.commentId,
    }
    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '好像没有登录噢~',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: '/pages/me/me',
            })
            return;
          }
        }
      })
    }

    if (that.data.comment_reply.length < 3) {
      wx.showModal({
        title: '提示',
        content: '至少输入三个字噢~',
      })
      return
    }

    that.setData({
      showDialog2: false,
    })
    wx, wx.showLoading({
      title: '稍等噢~',

    })

    wx.request({
      //url: getApp().globalData.url + '/addCommentReply/' + that.data.messageDetail.messageId,
      url: getApp().globalData.url+'add_message',
      method: "POST",
      data: list,
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: function(e) {
        wx.hideLoading()
        if (e.statusCode != 200) {
          wx.showModal({
            title: '提示',
            content: '服务器出现问题，请稍后再试',
          })
          return;
        }
        if (e.statusCode == 200) {
          wx.showModal({
            title: '提示',
            content: '回复成功~',
            success: function() {

              wx.request({
                //url: getApp().globalData.url + '/getMessageDetailById/' + that.data.messageDetail.messageId,
                url: getApp().globalData.url+'query_message_by_obj',
                method: "POST",
                data:{
                  "object_id": that.data.messageDetail.OBJECT_ID,
                },
                header:{
                  "content-type" : "application/x-www-form-urlencoded",
                  "chartset" : "utf-8",
                },
                success: function(e) {
                  
                  that.setData({
                    comment_reply: "",
                    user_comment: getcomment.comment(e.data.result),
                    user_reply: getcomment.reply(e.data.result),
                  })
                }
              })
            }
          })
        }

        if (e.data.code == 301) {
          wx.showModal({
            title: '提示',
            content: '你已被管理员禁止发布，详情请联系管理员',
            showCancel: false
          })
        }

      }
    })
  },
  /**
   * 回复数据
   */
  comment_reply(e) {
    this.setData({
      comment_reply: e.detail.value
    })
  },
  comment() {
    let that = this;

    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '好像没有登录噢~',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: "/pages/me/me"
            })
          }
        }
      })
      return
    }

    if (that.data.comment_input.length < 3) {
      wx.showModal({
        title: '提示',
        content: '至少输入三个字噢~',
        showCancel: false
      })
      return;
    }
    that.setData({
      showDialog1: false
    })
    wx.showLoading({
      title: '稍等噢~',
    })
    //console.log('comment_group_id:',that.data.comment_group_id)
    wx.request({
      //url: getApp().globalData.url + '/addComment/' + that.data.userId + '/' + that.data.messageDetail.messageId + '/' + that.data.messageDetail.userId,
      url: getApp().globalData.url+'add_message',
      method: "POST",
      data:{
        "group_id": that.data.comment_group_id,
        "openid": that.data.userId,
        "object_id": that.data.messageDetail.OBJECT_ID,
        "nick_name": that.data.userInfo.nickName,
        "gender": that.data.userInfo.gender,
        "target_id": that.data.messageDetail.OPEN_ID,
        "msg": that.data.comment_input,
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
            content: '服务器出现问题，请稍后再试',
          })
          return;
        }
        if (e.statusCode == 200) {

          wx.showModal({
            title: '提示',
            content: '留言成功',
            showCancel: false,
            success: function() {
              wx.request({
                //url: getApp().globalData.url + '/getMessageDetailById/' + that.data.messageDetail.messageId,
                url: getApp().globalData.url+'query_message_by_obj',
                method: "POST",
                data:{
                  "object_id": that.data.messageDetail.OBJECT_ID,
                },
                header:{
                  "content-type" : "application/x-www-form-urlencoded",
                  "chartset" : "utf-8",
                },
                success: function(e) {
                  
                  that.setData({
                    comment_input: "",
                    user_comment: getcomment.comment(e.data.result),
                    user_reply: getcomment.reply(e.data.result),
                    comment_group_id : that.data.comment_group_id+1,
                  })
                }
              })
            }
          })
        }
        if (e.data.code == 301) {
          wx.showModal({
            title: '提示',
            content: '你已被管理员禁止发布，详情请联系管理员',
            showCancel: false
          })
        }
      }
    })


  },
  /**
   * 删除信息
   */
  delete_message() {
    let that = this

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
            data:{
              "openid": that.data.userId,
              "object_id": that.data.messageDetail.OBJECT_ID,
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
              if (e.statusCode == 200) {
                wx.showModal({
                  title: '提示',
                  content: '删除成功',
                  showCancel: false,
                  success: function() {
                    wx.showLoading({
                      title: '更新主页信息中~',
                    })
                    that.updateAllMessage();
                    wx.hideLoading();
                  },

                })

              } else {
                wx.showModal({
                  title: '提示',
                  content: '非法操作，请联系管理员',
                  showCancel: false,
                  success: function() {
                    that.setData({
                      user_message: []
                    })
                    that.loadMessage(1)
                  }
                })
              }
            }
          })
        }
      }
    })
  },
  updateAllMessage() {
    let that = this;
    /**
     * 获取最新失物招领
     */
    // wx.request({
    //   url: getApp().globalData.url + '/getMessage/getLostMessage',
    //   method: "post",
    //   success: function(e) {
    //     getApp().globalData.lost_new = e.data
    //   }
    // })
    wx.request({
      //url: getApp().globalData.url + '/getMessage/getAllMessageDetail/' + 1,
      url: getApp().globalData.url+'query_latest_info',
      method: "POST",
      data:{
        "page_index": 0,
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: (res) => {
        getApp().globalData.messageDetail = res.data.result
      },
      complete: function() {
        wx.switchTab({
          url: '/pages/index/index',
        })
      }
    })
    getApp().globalData.isUpdate = 1;
  },
  /**
   * 收藏
   */
  collection() {
    let that = this;
    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '好像没有登录噢~',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: "/pages/me/me"
            })
          }
        }
      })
      return
    }

    if (that.data.messageDetail.NICK_NAME == "匿名者") {
      wx.showModal({
        title: '提示',
        content: '匿名信息无法收藏',
      })
      return
    }

    if (that.data.isCollection) {
      wx.request({
        //url: getApp().globalData.url + '/deleteCollection/' + that.data.userId + '/' + that.data.messageDetail.messageId,
        url: getApp().globalData.url+'del_attention',
        method: "POST",
        data:{
        "openid": getApp().globalData.userId,
        "object_id": that.data.messageDetail.OBJECT_ID,
        },
       header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
       },
        success: function(e) {
          if (e.statusCode != 200) {
            return
          }
          if (e.statusCode == 200) {
            that.setData({
              isCollection: false
            })
            wx.showModal({
              title: '提示',
              content: '已取消收藏',
            })
          }

        }
      })
    } else {
      wx.request({
        //url: getApp().globalData.url + '/add_attention/' + that.data.userId + '/' + that.data.messageDetail.messageId,
        url: getApp().globalData.url+'add_attention',
        method: "POST",
        data:{
        "openid": getApp().globalData.userId,
        "object_id": that.data.messageDetail.OBJECT_ID,
        },
        header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
        },
        success: function(e) {

          if (e.statusCode != 200) {
            return
          }
          if (e.statusCode == 200) {
            that.setData({
              isCollection: true
            })
            wx.showModal({
              title: '提示',
              content: '收藏成功！',
            })
          }
        }
      })
    }
  },
  onReady() {
    let that = this;
    /**页面渲染完毕 */
    setTimeout(function() {
      that.setData({
        isLoading: true
      })
    }, 500)
  },
  /**
   * 查看图片
   */
  look_image(e) {

    wx.previewImage({
      urls: [e.currentTarget.id],
    })
  },
  toggleDialog1(e) {
    this.setData({
      showDialog1: !this.data.showDialog1
    });
  },
  toggleDialog2(e) {
    this.setData({
      showDialog2: !this.data.showDialog2,
      liuyanName: e.target.dataset.name,
      commentUserId: e.target.id,
      group_id: e.target.dataset.group_id,
    });
  },
  toggleDialog3(e) {
    this.setData({
      showDialog3: !this.data.showDialog3,
      pinglunName: e.currentTarget.dataset.name,
      group_id: e.target.dataset.group_id,
      commentUserId: e.target.id,
    });
  },
  
  onLoad(options) {
    let that = this;
    this.setData({
      height: app.globalData.height,
      userInfo: getApp().globalData.userInfo,
      imageUrl:getApp().globalData.imageUrl,
    })

    wx.getStorage({
      key: 'userId',
      success: function(res) {
        that.setData({
          userId: res.data
        })
      },
    })
    
    wx.getStorage({
      key: 'userInfo',
      success: function(res) {
        that.setData({
          userInfo: res.data
        })
      },
    })


    this.setData({
      messageId: options.messageId
    })
    this.setData({
      userId: getApp().globalData.userId
    })

    //用户信息过期重新登陆
    if(this.data.userId==undefined)
    {
      wx.showModal({
        title: '提示',
        content: '用户信息过期，请重新登陆',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: "/pages/me/me"
            })
          }
        }
      })
    }

    var categoryname = options.messageId.slice(0,5);//取object_id前五个元素看是哪个类型
    that.setData({
      queryurl: getApp().globalData.querycategoryurl[judge.judgeurl(categoryname)],
      delurl: getApp().globalData.delmessageurl[judge.judgeurl(categoryname)]
    })

    wx.request({
      url: getApp().globalData.url + that.data.queryurl,
      method: "POST",
      data:{
        "condition": 'object_id',
        "value": options.messageId,
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: function(e) {
        if (e.statusCode != 200) {
          wx.showModal({
            title: '提示',
            content: '好像出问题啦，稍后再试吧~',
          })
          return
        }
        
        if (e.data == "" || e.data == null) {
          wx.showModal({
            title: '提示',
            content: '文章不存在或已被删除',
            showCancel: false,
            confirmColor: "返回",
            success: function() {
              wx.navigateBack({
                delta: 1
              })
            }
          })
          return
        }
        //console.log(e.data.result[0])
        that.setData({
          messageDetail: e.data.result[0]        
        })
      },
      complete: function() {


      }
    })

    that.setData({
      userIsAdmin: getApp().globalData.userIsAdmin
    })

    if (that.data.userId == -1) {
      wx.showModal({
        title: '提示',
        content: '你还没有登陆，请登陆',
        confirmText: "去登陆",
        success: function(e) {
          if (e.confirm) {
            wx.switchTab({
              url: "/pages/me/me"
            })
          }
        }
      })
      return;
    }

    wx.request({
      //url: getApp().globalData.url + '/addCollection/checkIsCollection/' + that.data.userId + '/' + options.messageId,
      url: getApp().globalData.url+'query_lost_found_attention_one',
      method: "POST",
      data:{
        "openid": getApp().globalData.userId,
        "object_id": options.messageId,
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: function(e) {
        if (e.statusCode != 200) {
          return
        }
        if (e.data.result == 1) {
          that.setData({
            isCollection: true
          })
        }
      }
    })
    /*
    获取留言信息
    */
   //console.log('obj_id:::',options.messageId)
    wx.request({
      //url: getApp().globalData.url + '/getMessageDetailById/' + that.data.messageDetail.messageId,
      url: getApp().globalData.url+'query_message_by_obj',
      method: "POST",
      data:{
        "object_id": options.messageId,
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: function(e) {
        //console.log(e.data.result[0])
        if(e.data.result==null||e.data.result.length==0||(e.data.result.length==1&&e.data.result[0].length==0))
        {
          return;
        }
      
        that.setData({
          comment_input: "",
          user_comment: getcomment.comment(e.data.result),
          user_reply: getcomment.reply(e.data.result),
        })
        //console.log('comment:',that.data.user_comment)
        that.setData({
          comment_group_id: e.data.result[e.data.result.length-1][0].GROUP_ID+1,
        })
        //console.log('onload：',that.data.comment_group_id)
      }
    })
    

    /*
  获取关注数
  */
    wx.request({
      //url: getApp().globalData.url + '/share/addShareCount/' + that.data.messageDetail.messageId,
      url: getApp().globalData.url+'query_attention_obj_size',
      method: "POST",
      data:{
        "object_id": options.messageId,
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success: function(e) {
        if (e.statusCode != 200) {
          return
        }
        if (e.statusCode == 200) {
          that.setData({
            attentionsize: e.data.result
          })
        }
      }
    })
  },

  /*
   更新转发信息
   */
  
   share_message(){
     var that = this
    var sharecategory = that.data.messageDetail.OBJECT_ID.slice(0,5);//取object_id前五个元素看是哪个类型
    wx.request({
      url: getApp().globalData.url+getApp().globalData.shareurl[judge.judgeurl(sharecategory)],
      method: "POST",
      data:{
        "object_id": that.data.messageDetail.OBJECT_ID,
      },
      header:{
        "content-type" : "application/x-www-form-urlencoded",
        "chartset" : "utf-8",
      },
      success:function(e){

      }
    })
   },

  /*
  更新留言信息 */
  comment_input(e) {
    this.setData({
      comment_input: e.detail.value
    })
  },
  onShareAppMessage(e) {
    return {
      title: "来看看~",
      success: function(res) {},
    }
  }
})