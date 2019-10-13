const brand_tweets_response = (response) => { 
        const data = response['data']['result']
        const filtered_data = data.map(( item) => {

            const text = clean_text(item.text)
            return {
                item,
                text
            }
        })
        return filtered_data


}

const clean_text = (text) => { 
        return text
        
}

export default brand_tweets_response