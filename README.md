Run instructions
```
    
```

Format of the normalized data    
```
    normalizedData
    [{
        hostname   :  '',    # compare dnsHostName and hostname
        ip_addr    :  '',    # compare address and local_ip
        manufacturer: '',    # compare bios_manufacturers
        platform   :  '',    # compare platform_name
        cloud      :  '',    # from cloudProvider
        os_version :  '',    # compare os_version aand os
       
        region     :  '',    # from region;
        # makes it easier to scale horizontally by region; whether mongo or whatever nosql you are using

        vendor_data:  [
            'vendor_name' : {
                # vendor details as it was received
            }
        ]
        # append all vendor data here WITHOUT modification
        # easier for audits AND protects you from legal.
    },....]
```