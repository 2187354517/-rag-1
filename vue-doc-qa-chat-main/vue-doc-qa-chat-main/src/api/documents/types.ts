interface DocParamsType {
  page_num: number
  page_size: number
  id?: string
  name?: string
  user_name?: string
}

interface ResponseDocPageType {
  page_num: number
  page_size: number
  total: number
  list: DocTableType[]
}

interface DocTableType {
  id: string
  name: string
  file_name: string
  file_path: string
  suffix: string
  vector: string
  date: string
  user_name: string
}

export type { DocParamsType, ResponseDocPageType, DocTableType }
