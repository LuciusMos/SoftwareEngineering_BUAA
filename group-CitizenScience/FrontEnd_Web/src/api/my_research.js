import request from '@/utils/request'

export function getMyResearchList(params) {
  return request({
    url: '/vue-admin-template/myResearch/list',
    method: 'get',
    params
  })
}
