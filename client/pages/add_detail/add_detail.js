//index.js
//获取应用实例
const app = getApp()
//var uploadImage = require('../../utils/uploadFile.js');
var util = require('../../utils/util.js');


Page({
  data: {
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '发布-详情', //导航栏 中间的标题
      height: 0
    },
    userId: -1,
    // 此页面 页面内容距最顶部的距离
    height: app.globalData.height * 2 + 20,
    result_image_url: [],
    next_obj_id: "",
    img_list: [],
    img_url: [],
    hideAdd: false,
    array: [],
    gradearray: [15,16,17,18,19,20],
    classarray: ['钱包','钥匙','宠物','卡类/证照','数码产品','书籍/文件','衣服/鞋帽','首饰/挂饰','行李/包裹','手袋/挎包','其它'],
    category_index:  null,
    grade_index: null,
    class_index: null,
    categoryurl: [],
    querycategoryurl: [],
    messagelength: 0,
    input_intro: "",
    input_phone: "",
    input_level: "",
    input_major: "",
    input_anonymity: false,
    input_subject: "",
    input_obj_name: "",
    //input_obj_class: "",
  },
  input_intro: function(e) {
    let value = e.detail.value;
    this.setData({
      input_intro: value
    })
  },
  input_phone: function(e) {
    let value = e.detail.value;
    this.setData({
      input_phone: value
    })
  },
  // input_level: function(e) {
  //   let value = e.detail.value;
  //   this.setData({
  //     input_level: value
  //   })
  // },
  input_major: function(e) {
    let value = e.detail.value;
    this.setData({
      input_major: value
    })
  },
  input_obj_name: function(e) {
    let value = e.detail.value;
    this.setData({
      input_obj_name: value
    })
  },
  // input_obj_class: function(e) {
  //   let value = e.detail.value;
  //   this.setData({
  //     input_obj_class: value
  //   })
  // },
  input_subject: function(e) {
    let value = e.detail.value;
    this.setData({
      input_subject: value
    })
  },

  onLoad() {
    this.setData({
      height: app.globalData.height
    })
    var arrays = [];
    for (var i = 0; i < getApp().globalData.categoryid.length; i++) {
      arrays.push(getApp().globalData.categoryname[i])
    }
    this.setData({
      array: arrays
    })

    this.setData({
      categoryurl: getApp().globalData.categoryurl,
      querycategoryurl: getApp().globalData.querycategoryurl
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
  },
  /**
   * 删除选择的图片
   */
  deleteImg: function(res) {

    let that = this;
    wx.showModal({
      title: '提示',
      content: '是否删除',
      success: function(e) {
        if (e.confirm) {
          var image = [];
          var i = 0;
          for (var j = 0; j < that.data.img_url.length; j++) {
            if (that.data.img_url[j] != res.target.id) {
              image.push(that.data.img_url[j])
            }
          }
          that.setData({
            img_url: image
          })
          if (that.data.img_url.length < 9) {
            that.setData({
              hideAdd: false
            })
          } else {
            that.setData({
              hideAdd: true
            })
          }
        }

      }
    })

  },
  /**
   * 匿名开关
   */
  switch1Change() {
    this.setData({
      input_anonymity: !this.data.input_anonymity
    })
  },
  chooseimage: function() {
    var that = this;
    wx.chooseImage({
      count: 9 - that.data.img_url.length, // 默认9 
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有 
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有 
      success: function(res) {

        if (res.tempFilePaths.length > 0) {
          //图如果满了9张，不显示加图
          if (that.data.img_url.length == 9) {
            that.setData({
              hideAdd: true
            })
          } else {
            that.setData({
              hideAdd: false
            })
          }
          //把每次选择的图push进数组
          let img_url = that.data.img_url;

          for (let i = 0; i < res.tempFilePaths.length; i++) {
            if (i <= 8) {
              img_url.push(res.tempFilePaths[i])
            }

          }
          that.setData({
            img_url: img_url
          })
          /**
           * 如果选择多于九张,停止添加
           */

          if (that.data.img_url.length == 9) {
            that.setData({
              hideAdd: true
            })
          } else {
            that.setData({
              hideAdd: false
            })
          }
        }
      }
    })
  }, //图片上传
  img_upload: function(res) {
    let that = this;
    let img_url = that.data.img_url;
    let img_list = that.data.img_list;
    // let images_url = [];
    let i =res.i;
    //由于图片只能一张一张地上传，所以用循环，不过为了保证上传成功，改为递归调用 
        wx.showLoading({
          title: '上传中' + (i + 1) + '/' + img_url.length,
          mask: true
        })
        //console.log(img_url[i])
        //上传图片
        //你的域名下的/images/文件下的/当前年月日文件下的/图片.png
        //图片路径可自行修改
        
        if(i==0){
          img_list.next_image = 'first';
        }else{
          img_list.next_image = that.data.next_obj_id;
          console.log('img_list',img_list)
        }
        console.log('i:',i)
        wx.uploadFile({
          filePath: img_url[i],
          name: 'files',
          url: getApp().globalData.url+that.data.categoryurl[that.data.category_index],
          formData: img_list,
          success: function(e) {
            //console.log('e.data:',e.data)
            if(i==0){
              that.setData({
                next_obj_id: e.data.replace("\"","").replace("\"","")
              })
              //console.log(that.data.next_obj_id)
            }
            // images_url.push(img_url[i]);//多图实现需要
            wx.hideLoading()
            if (e.statusCode != 200) {
              wx.showModal({
                title: '提示',
                content: '服务器出现问题啦，请稍后再试~',
              })
              return;
            }

            if(e.data=="error")
            {
              wx.showModal({
                title: '提示',
                content: '发布出现问题啦，请联系管理员或稍后再试~',
              })
              return;
            }
            // if (e.statusCode == 200&& i == img_url.length-1) {
              
            // }
            if (e.data.code == 301) {
              wx.showModal({
                title: '提示',
                content: '你已被管理员禁止发布，详情请联系管理员',
                showCancel: false
              })
            }
          },
          complete:function(){
            //console.log('complete:',i);
            i++;
            if(i==img_url.length){//图片传完停止调用
              wx.showModal({
                title: '提示',
                content: '发布成功',
                showCancel: false,
                success: function(res) {
                  if (res.confirm) {
                    wx.showLoading({
                      title: '更新主页信息中~',
                    })
                    getApp().globalData.isUpdate = 1
                    wx.switchTab({
                      url: '/pages/index/index',
                    })
                  }
                }
              })
            }else {
              res.i = i;
              that.img_upload(res);
            }
          }
        })
  },
  isPhone(val) {

    var isPhone = /^[1](([3][0-9])|([4][5-9])|([5][0-3,5-9])|([6][5,6])|([7][0-8])|([8][0-9])|([9][1,8,9]))[0-9]{8}$/; //手机号码
    var isMob = /^0?1[3|4|5|8][0-9]\d{8}$/; // 座机格式
    if (isMob.test(val) || isPhone.test(val)) {

      return true;
    } else {

      return false;
    }
  },
  //去左右空格;
  trim(s) {
    return s.replace(/(^\s*)|(\s*$)/g, "");
  },
  submit() {


    var that = this;



    if (that.trim(that.data.input_intro) == "" || that.trim(that.data.input_intro) < 2) {
      wx.showModal({
        title: '提示',
        content: '内容有点少噢~(至少两个字)',
        showCancel: false
      })
      return;
    }
    if (!that.isPhone(that.data.input_phone)) {
      wx.showModal({
        title: '提示',
        content: '手机格式不对噢~',
        showCancel: false
      })
      return;
    }
    // if (new Number(that.data.input_level) < 14 || new Number(that.data.input_level) > 20) {
    //   wx.showModal({
    //     title: '提示',
    //     content: '年级不对噢~',
    //     showCancel: false
    //   })
    //   return;
    // }
    if (that.trim(that.data.input_major) < "" || that.trim(that.data.input_major).length < 3) {
      wx.showModal({
        title: '提示',
        content: '专业貌似不对噢~',
        showCancel: false
      })
      return;
    }

    // if ((that.trim(that.data.input_subject) < "" || that.trim(that.data.input_subject).length < 2)&&(that.data.category_index==1||that.data.category_index==2)) {
    //   wx.showModal({
    //     title: '提示',
    //     content: 'subject貌似不对噢~',
    //     showCancel: false
    //   })
    //   return;
    // }

    if (that.data.category_index == null) {
      wx.showModal({
        title: '提示',
        content: '选择一个分类噢~',
        showCancel: false
      })
      return;
    }
    if (that.data.grade_index == null) {
      wx.showModal({
        title: '提示',
        content: '选择你的年级噢~',
        showCancel: false
      })
      return;
    }
    if ((that.data.category_index==0||that.data.category_index==3)&&that.data.class_index == null) {
      wx.showModal({
        title: '提示',
        content: '选择一个类别噢~',
        showCancel: false
      })
      return;
    }
    wx.showModal({
      title: '提示',
      content: '是否发布',
      success: function(e) {
        if (e.confirm) {

          wx.showLoading({
            title: '发布中~',
          })
          console.log("userid:",that.data.userId)
          let list = that.data.category_index==0||that.data.category_index==3?{
          /*
          失物招领+闲置交易
          */
          openid: that.data.userId,
          object_name : that.data.input_obj_name,
          object_class : that.data.classarray[that.data.class_index],
          msg: "物品名称："+that.data.input_obj_name+"\n"+"物品类别："+that.data.classarray[that.data.class_index]+"\n"+that.data.input_intro,
          phone: that.data.input_phone,
          grade: that.data.gradearray[that.data.grade_index]+"级",
          major: that.data.input_major,
          gender: getApp().globalData.userInfo.gender,
          nick_name: that.data.input_anonymity?"匿名者":getApp().globalData.userInfo.nickName
          }:{
            
              /*
              相约学习+约个球+其它四个模块
              */
              openid: that.data.userId,
              //obj_name : that.data.input_obj_name,
              //obj_class : that.data.input_obj_class,
              subject: that.data.input_subject,
              msg: that.data.input_intro,
              phone: that.data.input_phone,
              grade: that.data.gradearray[that.data.grade_index]+"级",
              major: that.data.input_major,
              gender: getApp().globalData.userInfo.gender,
              nick_name: that.data.input_anonymity?"匿名者":getApp().globalData.userInfo.nickName
          }
          that.setData({
            img_list: list
          })
          
          if (that.data.userId == -1) {
            wx.showModal({
              title: '提示',
              content: '数据出现错误,请稍后重试',
            })
            return;
          }

          if(that.data.img_url.length>0)
          {
            var data =[];
            data.timestamp  = Date.parse(new Date()) / 1000;  //当前时间戳
            data.i = 0;
            that.img_upload(data);
          }         
          else{
            wx.request({
              url: getApp().globalData.url+that.data.categoryurl[that.data.category_index],
              method: "POST",
              data: list,
              header:{
                "content-type" : "application/x-www-form-urlencoded",
                "chartset" : "utf-8",
              },
              success: e=> {
                console.log(e.data)
                wx.hideLoading()
                if (e.statusCode != 200) {
                  wx.showModal({
                    title: '提示',
                    content: '服务器出现问题啦，请稍后再试~',
                  })
                  return;
                }
  
                if (e.statusCode == 200) {
                  wx.showModal({
                    title: '提示',
                    content: '发布成功',
                    showCancel: false,
                    success: function(res) {
                      if (res.confirm) {
                        wx.showLoading({
                          title: '更新主页信息中~',
                        })
                        wx.request({
                          url: getApp().globalData.url + that.data.querycategoryurl[that.data.category_index],
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
                            var arr = res.data.result.slice(0,1);
                            that.data.messagelength=getApp().globalData.messageDetail.unshift(arr);
                            /**
                             * 获取最新失物招领
                             */
                            // wx.request({
                            //   url: getApp().globalData.url + '/getMessage/getLostMessage',
                            //   method: "post",
                            //   success: function(e) {
                            //     getApp().globalData.lost_new = e.data
                            //     wx.hideLoading();
                            //   },
 
                            // })
                          },                          
                          complete: function() {
                            getApp().globalData.isUpdate = 1
                            wx.switchTab({
                              url: '/pages/index/index',
                            })
                          }
                        })
                      }
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
          }
          
        }
      }
    })

  },
  //获取选定滑动框的索引
  bindPickerChange: function(e) {
    this.setData({
      category_index: e.detail.value
    })

  },
  bindPickerChange_grade:function(e) {
    this.setData({
      grade_index: e.detail.value
    })
  },
  bindPickerChange_class:function(e) {
    this.setData({
      class_index: e.detail.value
    })
  }

})