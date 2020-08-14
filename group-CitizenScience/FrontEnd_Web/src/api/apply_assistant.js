import request from '@/utils/request'

export function getApplyAssistantList(params) {
  return request({
    url: '/vue-admin-template/apply_assistant/list',
    method: 'get',
    params
  })
}
