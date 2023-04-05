export const timestampFormat = (str: string, now: number) => {
    const date = new Date(str)

    const seconds = Math.floor((now - (date as any)) / 1000)

    let interval = seconds / 31536000

    if (interval > 2) {
        return Math.floor(interval) + " years"
    }
    if (interval > 1) {
        return "1 year"
    }
    interval = seconds / 2592000
    if (interval > 2) {
        return Math.floor(interval) + " months"
    }
    if (interval > 1) {
        return "1 month"
    }
    interval = seconds / 86400
    if (interval > 2) {
        return Math.floor(interval) + " days"
    }
    if (interval > 1) {
        return "1 day"
    }
    interval = seconds / 3600
    if (interval > 2) {
        return Math.floor(interval) + " hours"
    }
    if (interval > 1) {
        return "1 hour"
    }
    interval = seconds / 60
    if (interval > 2) {
        return Math.floor(interval) + " minutes"
    }
    if (interval > 1) {
        return "1 minute"
    }
    return "<1 minute"
}