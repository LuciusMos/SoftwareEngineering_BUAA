import request from '@/utils/request'

export function getVolunteerList(params) {
  return request({
    url: '/vue-admin-template/menu1/volunteer/list',
    method: 'get',
    params
  })
}
