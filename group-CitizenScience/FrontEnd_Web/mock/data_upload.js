import Mock from 'mockjs'

const data = Mock.mock({
  'items|30': [{
    id: '@id',
    researchName: '@id'
  }]
})

export default [
  {
    url: '/vue-admin-template/data_upload/list',
    type: 'get',
    response: config => {
      const items = data.items
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items
        }
      }
    }
  }
]
