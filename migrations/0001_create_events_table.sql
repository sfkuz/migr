CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    genre TEXT,
    event_type TEXT,
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ,
    organizer_name TEXT NOT NULL,
    url TEXT NOT NULL,
    cover_image_url TEXT,
    price INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CREATE INDEX id_events_start_at ON events(start_at)
    CREATE INDEX id_events_event_type ON events(event_type)

    CONSTRAINT events_title_not_blank CHECK (btrim(title) <> ''),
    CONSTRAINT events_organizer_not_blank CHECK (btrim(organizer_name) <> ''),
    CONSTRAINT events_url_not_blank CHECK (btrim(url) <> ''),
    CONSTRAINT events_dates_check CHECK (end_at is null or end_at > start_at),
    CONSTRAINT events_price_positive CHECK (price is null or price >= 0),

    CREATE TRIGGER trg_event_set_updated_at
    BEFORE UPDATE ON events
    FOR EACH ROW
    EXECUTE FUNCTION app_private.set_updated_at();
)