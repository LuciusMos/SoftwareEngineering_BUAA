<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  tagFilter: {
    publicFilter(status) {
      const publicMap = {
        公开: "success",
        非公开: "danger"
      };
      return publicMap[status];
    },
    statusFilter(status) {
      const statusMap = {
        已通过: "success",
        待审核: "warning",
        数据收集: "success",
        数据分析: "success",
        已结项: "info",
        未通过: "danger",
        重新审核:"warning"
      };
      return statusMap[status];
    },
    rateFilter(rate) {
      const rateMap = {
        0: "info",
        1: "warning",
        2: "warning",
        3: "",
        4: "",
        5: "success"
      };
      return rateMap[rate];
    },
    identityFilter(iden) {
      const identityMap = {
        1: "info",
        2: "primary",
        3: "success"
      };
      return identityMap[iden];
    }
  },

  branch: [
    "经济",
    "社会",
    "教育",
    "心理",
    "文学",
    "物理",
    "化学",
    "动物",
    "植物",
    "微生物",
    "地理",
    "大气",
    "生态",
    "天文",
    "水文",
    "建筑",
    "农业",
    "医学",
    "艺术",
    "管理学",
    "新闻传媒",
    "信息技术"
  ],
  dataType: [
    {
      value: 1,
      label: "小数"
    },
    {
      value: 2,
      label: "整数"
    },
    {
      value: 3,
      label: "文本"
    },
    // {
    //   value: 4,
    //   label: "分数"
    // },
    {
      value: 5,
      label: "图片"
    },
    // {
    //   value: 6,
    //   label: "视频"
    // },
    // {
    //   value: 7,
    //   label: "音频"
    // },
    {
      value: 8,
      label: "类别"
    },
    {
      value: 9,
      label: "位置"
    }
  ],
  formRules: {
    name: [
      { required: true, message: "请输入项目名称", trigger: "blur,change" },
      {
        min: 0,
        max: 18,
        message: "字数请控制在18字以内",
        trigger: "blur,change"
      }
    ],
    date1: [
      { required: true, message: "请选择起止时间", trigger: "blur,change" }
    ],
    // date2: [
    //   { required: true, message: "请选择起止时间", trigger: "blur,change" }
    // ],
    endDate: [
      { required: true, message: "请选择结项时间", trigger: "blur,change" }
    ],
    public: [
      {
        required: true,
        message: "请设置项目是否公开",
        trigger: "blur,change"
      }
    ],
    participate_way: [
      { required: true, message: "请设置参与方式", trigger: "blur,change" },
      {
        min: 0,
        max: 200,
        message: "字数请控制在200字以内",
        trigger: "blur,change"
      }
    ],
    branch: [
      { required: true, message: "请设置项目学科", trigger: "blur,change" }
    ],
    type: [
      {
        required: true,
        message: "请至少输入一个项目类型",
        trigger: "blur,change"
      }
    ],
    desc: [
      { required: true, message: "请填写项目描述", trigger: "blur,change" },
      {
        min: 0,
        max: 500,
        message: "字数请控制在500字以内",
        trigger: "blur,change"
      }
    ],
    background: [
      {
        required: false,
        message: "请填写背景资料",
        trigger: "blur,change"
      },
      {
        min: 0,
        max: 2000,
        message: "字数请控制在2000字以内",
        trigger: "blur,change"
      }
    ],
    note: [
      {
        required: false,
        message: "请填写注意事项",
        trigger: "blur,change"
      },
      {
        min: 0,
        max: 500,
        message: "字数请控制在500字以内",
        trigger: "blur,change"
      }
    ],
    assistants: [{}],
    pic: [{ required: true, message: "请设置项目主图", trigger: "blur,change" }]
  },
  server: "http://114.115.129.146:8000/",
  noPortServer: "http://114.115.129.146/"
  // server: 'http://127.0.0.1:5000/',
  // noPortServer: 'http://127.0.0.1/'
};
</script>
