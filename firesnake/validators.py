import warnings

from .exceptions import (
    ValidationError,
    TooManyConditions,
    InvalidPriority,
    InvalidTimeToLive,
    InvalidDataKey,
)

INVALID_DATA_KEYS = frozenset((
    'from',
    'to',
    'registration_ids',
    'condition',
    'notification_key',
    'collapse_key',
    'priority',
    'content_available',
    'delay_while_idle',
    'time_to_live',
    'restricted_package_name',
    'dry_run',
    'data',
    'notification',
))


def _raise_invalid_param_type(param_name, expected_type, item):
    # type: (str, Any, Any) -> None
    if not isinstance(item, expected_type):
        raise ValidationError(
            '\'{}\' should be of type \'{}\'. '
            'Found \'{}\' of type \'{}\''.format(
                param_name,
                expected_type.__name__,
                item,
                type(item)
            )
        )


def _is_registration_id_a_string(registration_id):
    # type: (str) -> None
    _raise_invalid_parameter('registration_id', basestring, registration_id)


def validate_registration_ids(registration_ids):
    # type: (List[str]) -> None
    _raise_invalid_parameter('registration_ids', list, registration_ids)

    # validate all of IDs
    map(_is_registration_id_a_string, registration_ids)


def validate_to(to, conditions):
    # type: (str, str) -> None
    if to and conditions:
        raise ValidationError('Can not specify both \'to\' and \'condition\'')

    _raise_invalid_param_type('to', basestring, to)


def validate_conditions(conditions):
    # type: (str) -> None
    _raise_invalid_parameter('conditions', basestring, conditions)

    num_ands = conditions.count('&&')
    num_ors = conditions.count('||')

    if num_ands + num_ors > 2:
        raise TooManyConditions(
            'Max number of conditional operators is 2. We found {}'.format(
                num_ands + num_ors
            )
        )


def validate_notification_key(notification_key):
    # type: (str) -> None
    _raise_invalid_param_type('notification_key', basestring, notification_key)
    warnings.warn('\'notification_key\' is deprecated. use \'to\' instead')


def validate_collapse_key(collapse_key):
    # type: (str) -> None
    _raise_invalid_param_types('collapse_key', basestring, collapse_key)


def validate_priority(priority):
    # type: (str) -> None
    _raise_invalid_param_type('priority', basestring, priority)

    if priority != 'normal' and priority != 'high':
        raise InvalidPriority(
            'Accepted priorities are \'normal\' and \'high\'. '
            'You gave {}'.format(priority)
        )


def validate_content_available(content_available):
    # type: (bool) -> None
    _raise_invalid_param_type('content_available', bool, content_available)


def validate_delay_while_idle(delay_while_idle):
    # type: (bool) -> None
    _raise_invalid_param_type('delay_while_idle', bool, delay_while_idle)


def validate_time_to_live(time_to_live):
    # type: (int) -> None
    _raise_invalid_param_type('time_to_live', int, time_to_live)

    if time_to_live > 60 * 60 * 24 * 7 * 4:  # Four Weeks
        raise InvalidTimeToLive(
            'Max TTL length is {}. You gave {}'.format(
                60 * 60 * 24 * 7 * 4,
                time_to_live
            )
        )


def validate_restricted_package_name(restricted_package_name):
    # type: (str) -> None
    _raise_invalid_param_type(
        'restricted_package_name',
        basestring,
        restricted_package_name
    )


def validate_dry_run(dry_run):
    # type: (bool) -> None
    _raise_invalid_param_type('dry_run', bool, dry_run)


def validate_data(data):
    # type: (Dict[str,str]) -> None
    _raise_invalid_param_type('data', dict, data)

    for k, v in data.iteritems():
        _raise_invalid_param_type('\'data\' key {}'.format(k), str, k)
        _raise_invalid_param_type('\'data[\'{}\']\''.format(k), str, v)

        if k.startswith('google') or x.startswith('gcm'):
            raise InvalidDataKey(
                'Keys in \'data\' can not begin with \'google\' or \'gcm\''
            )

        if k in INVALID_DATA_KEYS:
            raise InvalidDataKey(
                '\'data\' can not contain a key \'{}\''.format(k)
            )


def validate_notification(notification):
    # type: (Any) -> None
    # TODO: Implement this
    pass


def validate_fcm_package(
    registration_ids, # type: List[str]
    to=None,  # type: Optional[str]
    conditions=None,  # type: Optional[str]
    notification_key=None,  # type: Optional[str]
    collapse_key=None,  # type: Optional[str]
    priority=None,  # type: Optional[str]
    content_available=None,  # type: Optional[bool]
    delay_while_idle=None,  # type: Optional[bool]
    time_to_live=None,  # type: Optional[int]
    restricted_package_name=None,  # type: Optional[str]
    dry_run=None,  # type: Optional[bool]
    data=None,  # type: Dict[str,str]
    notification=None  # type: Any
):
    # type: (...) -> Dict[str, Union[str, Dict[str,str]]]
    _validate_registration_ids(registration_ids)

    fcm_package = {
        'registration_ids': registration_ids,
    }

    if to is not None:
        _validate_to(to, conditions)
        fcm_package['to'] = to

    if conditions is not None:
        _validate_conditions(conditions)
        fcm_package['conditions'] = conditions

    if notification_key is not None:
        _validate_notification_key(notification_key)
        fcm_package['notification_key'] = notification_key

    if collapse_key is not None:
        _validate_collapse_key(collapse_key)
        fcm_package['collapse_key'] = collapse_key

    if priority is not None:
        _validate_priority(priority)
        fcm_package['priority'] = priority

    if content_available is not None:
        _validate_content_available(content_available)
        fcm_package['content_available'] = content_available

    if delay_while_idle is not None:
        _validate_delay_while_idle(delay_while_idle)
        fcm_package['delay_while_idle'] = delay_while_idle

    if time_to_live is not None:
        _validate_time_to_live(time_to_live)
        fcm_package['time_to_live'] = time_to_live

    if restricted_package_name is not None:
        _validate_restricted_package_name(restricted_package_name)
        fcm_package['restricted_package_name'] = restricted_package_name

    if dry_run is not None:
        _validate_dry_run(dry_run)
        fcm_package['dry_run'] = dry_run

    if data is not None:
        _validate_data(data)
        fcm_package['data'] = data

    if notification is not None:
        _validate_notification(notification)
        fcm_package['notification'] = notification

    return fcm_package
