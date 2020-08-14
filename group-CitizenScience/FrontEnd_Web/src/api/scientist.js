import request from '@/utils/request'

export function getScientistList(params) {
  return request({
    url: '/vue-admin-template/menu1/scientist/list',
    method: 'get',
    params
  })
}
