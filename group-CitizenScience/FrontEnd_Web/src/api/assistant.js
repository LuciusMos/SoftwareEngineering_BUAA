import request from '@/utils/request'

export function getAssistantList(params) {
  return request({
    url: '/vue-admin-template/menu1/assistant/list',
    method: 'get',
    params
  })
}
